package net.bangniji.recommendation.util;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.regex.Pattern;

public class WordProcessor {
	private static HashSet<String> stopWords;
	static{
		String stopWd="I a about an are as at be by com for from";
		stopWd += "in is it of on or that the this to was what";
		stopWd += "when wheres who will with the www";
		
		for (String word : stopWd.split(" ")) {
			stopWords.add(word);
		}
	}

	public static List<String> process(String str) {
		List<String> result = new ArrayList<String>();
		
		str = str.toLowerCase();
		String[] words = str.split(" ");
		for (String word : words) {
			List<String> tmp = split(word);
			result.addAll(tmp);
		}
		
		return result;
	}
	
	private static List<String> split(String str) {
		Pattern p = Pattern.compile("[^a-zA-Z0-9]");
		List<String> result = new ArrayList<String>();
		
		String[] words = p.split(str);
		for(String s : words) {
			if (s.length() > 1) {
				if (! stopWords.contains(s)) { // not stop word
					result.add(s);
				}
			}
		}
		
		return result;
	}
}
