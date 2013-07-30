package net.bangniji.recommendation.service.impl;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map.Entry;
import java.util.Set;

import javax.jws.WebService;
import org.bson.types.ObjectId;

import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import net.bangniji.recommendation.service.inf.IRecommendation;
import net.bangniji.recommendation.util.MongoDBOper;
import net.bangniji.recommendation.util.WordProcessor;

@WebService(endpointInterface="net.bangniji.recommendation.service.inf.IRecommendation")
public class RecommendationSrv implements IRecommendation {
	private String serverHost = "10.0.58.13";
	private int port = 30000;
	private String dbName = "documentdatabase";
	public static final int TITLEWEIGHT = 3;
	public static final int RECNUM = 5;
	
	@Override
	public List<String> getRecommendation(String content) {
		// TODO Auto-generated method stub
		MongoClient cli = MongoDBOper.getClient(serverHost, port);
		DB db = cli.getDB(dbName);
		DBCollection invertedIndexCol = db.getCollection("invertedIndex");
		DBCollection literatureAssetCol = db.getCollection("literatureasset");
		
		List<String> targetWords = WordProcessor.process(content);
		HashSet<String> wordSpace = new HashSet<String>();
		HashMap<String, Double> idf = new HashMap<String, Double>();
		HashSet<String> documentSpace = new HashSet<String>();
		
		for(String word : targetWords) {
			if (wordSpace.add(word)) {
				BasicDBObject query = new BasicDBObject("_id", word);
				DBCursor cursor = invertedIndexCol.find(query);
				if (cursor.hasNext()) {
					DBObject obj = cursor.next();
					String docIds = (String) obj.get("value");
					Double idfValue = (Double) obj.get("idf");
					idf.put(word, idfValue);
					for (String docId : docIds.split(",")) {
						documentSpace.add(docId);
					}
				}
			}
		}
		
		HashMap<String, HashMap<String, Integer>> vectorSpace = new HashMap<String, HashMap<String, Integer>>();
		HashMap<String, Integer> targetVecSpace = new HashMap<String, Integer>();// 目标向量空间
		for(String word : targetWords) {
			if (targetVecSpace.get(word) == null) {
				targetVecSpace.put(word, 1);
			} else {
				int value = targetVecSpace.get(word).intValue() + 1;
				targetVecSpace.put(word, value);
			}
		}
		
		for(String docId : documentSpace) {
			ObjectId oId = new ObjectId(docId);
			BasicDBObject query = new BasicDBObject("_id", oId);
			DBCursor cursor = literatureAssetCol.find(query);
			
			HashMap<String, Integer> vecSpace = new HashMap<String, Integer>();
			
			if (cursor.hasNext()) {
				DBObject obj = cursor.next();
				String title = (String) obj.get("title");
				String literatureAbstract = (String) obj.get("literatureAbstract");
				
				// 处理标题
				if (title != null && title.length() > 0) {
					List<String> words = WordProcessor.process(title);
					for(String word : words) {
						// 添加到词空间
						wordSpace.add(word);
						
						// 添加相应的idf
						BasicDBObject q = new BasicDBObject("_id", word);
						DBCursor c = invertedIndexCol.find(q);
						if (c.hasNext()) {
							DBObject pobj = c.next();
							Double idfValue = (Double) pobj.get("idf");
							idf.put(word, idfValue);
						}
						
						// 添加tf值
						if (vecSpace.get(word) == null) {
							vecSpace.put(word, TITLEWEIGHT);
						} else {
							int value = vecSpace.get(word).intValue();
							value += TITLEWEIGHT;
							vecSpace.put(word, value);
						}
					}
				}
				
				// 处理摘要
				if (literatureAbstract != null && literatureAbstract.length() > 0) {
					List<String> words = WordProcessor.process(literatureAbstract);
					for(String word : words) {
						// 添加到词空间
						wordSpace.add(word);
						
						// 添加相应的idf
						BasicDBObject q = new BasicDBObject("_id", word);
						DBCursor c = invertedIndexCol.find(q);
						if (c.hasNext()) {
							DBObject pobj = c.next();
							Double idfValue = (Double) pobj.get("idf");
							idf.put(word, idfValue);
						}
						
						// 添加tf值
						if (vecSpace.get(word) == null) {
							vecSpace.put(word, 1);
						} else {
							int value = vecSpace.get(word).intValue();
							value += 1;
							vecSpace.put(word, value);
						}
					}
				}
			}
			
			vectorSpace.put(docId, vecSpace);
		}
		
		HashMap<String, Double> similarity = new HashMap<String, Double>();
		
		Set<String> tgWords = new HashSet<String>(targetWords);
		for (String docId : vectorSpace.keySet()) {
			// 计算向量相似度
			HashMap<String, Integer> docVec = vectorSpace.get(docId);
			Set<String> docWords = docVec.keySet();
			docWords.retainAll(tgWords); // interaction
			
			double product = 0.0;
			for(String word : tgWords) {
				double idfValue = idf.get(word);
				double tgTf = targetVecSpace.get(word);
				double docTf = docVec.get(word);
				
				product += tgTf * idfValue * docTf * idfValue;
			}
			
			double tmp = 0.0;
			for (String word : tgWords) {
				double value = idf.get(word) + targetVecSpace.get(word);
				tmp += value * value;
			}
			
			double tgVecValue = Math.sqrt(tmp);
			
			tmp = 0.0;
			for (String word : docVec.keySet()) {
				double value = idf.get(word) + docVec.get(word); // TF * IDF
				tmp += value * value;
			}
			
			double docVecValue = Math.sqrt(tmp);
			
			double sim = product / (docVecValue * tgVecValue);
			similarity.put(docId, sim);
		}
		
		List<Entry<String, Double>> tmpList = new ArrayList<Entry<String, Double>>(similarity.entrySet());
		
		// sort the similarity
		Collections.sort(tmpList, new Comparator<Entry<String, Double>>(){
			public int compare(Entry<String, Double> o1, Entry<String, Double> o2) {
				double v = o2.getValue().doubleValue() - o1.getValue().doubleValue();
				
				if (v > 0) {
					return 1;
				} else if ( v < 0) {
					return -1;
				} else {
					return 0;
				}
			}
		});
		
		List<String> result = new ArrayList<String>();
		for(int i = 0; i < RECNUM; ++i) {
			result.add(tmpList.get(i).getKey());
		}
		return result;
	}
}
