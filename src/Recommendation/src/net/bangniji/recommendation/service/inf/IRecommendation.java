package net.bangniji.recommendation.service.inf;

import java.util.List;

import javax.jws.WebService;

@WebService
public interface IRecommendation {
	public List<String> getRecommendation(String content);
}
