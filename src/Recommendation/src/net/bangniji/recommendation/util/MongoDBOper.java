package net.bangniji.recommendation.util;

import java.net.UnknownHostException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import com.mongodb.MongoClient;
import com.mongodb.DB;

public class MongoDBOper {
	private static final Logger log = LoggerFactory.getLogger(MongoDBOper.class);
	public static MongoClient getClient(String host, int port)  {
		synchronized(MongoDBOper.class) {
			if (dbClient == null) {
				try {
					dbClient = new MongoClient(host, port);
				} catch (UnknownHostException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
		return dbClient;
	}
	
	private static MongoClient dbClient = null;
}
