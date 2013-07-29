package net.bangniji.recommendation.service.impl;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

import javax.annotation.Resource;
import javax.jws.WebService;
import javax.xml.ws.WebServiceContext;

import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import com.sun.xml.bind.v2.runtime.unmarshaller.XsiNilLoader.Array;

import net.bangniji.recommendation.service.inf.IRecommendation;
import net.bangniji.recommendation.util.MongoDBOper;
import net.bangniji.recommendation.util.WordProcessor;

@WebService(endpointInterface="net.bangniji.recommendation.service.inf.IRecommendation")
public class RecommendationSrv implements IRecommendation {
	private String serverHost = "localhost";
	private int port = 27017;
	private String dbName = "test";
	
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
		return null;
	}
}
