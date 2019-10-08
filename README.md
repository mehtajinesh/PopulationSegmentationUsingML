# PopulationSegmentationUsingML
	1. Problem statement : Population segmentation aims to find natural groupings in population data that reveal some feature-level similarities between different regions in the US.
	2. Note : Need conda_mxnet_p36 [provides some in built frameworks] or use conda_pytorch_p36.
	
	3. Steps : 
		• Data loading and exploration
		• Data cleaning and pre-processing
		• Dimensionality reduction with PCA
		• Feature engineering and data transformation
		• Clustering transformed data with k-means
		• Extracting trained model attributes and visualizing k clusters
		
	4. Process : Using principal component analysis (PCA) you will reduce the dimensionality of the original census data. Then, you'll use k-means clustering to assign each US county to a particular cluster based on where a county lies in component space. 
	
	5. Uses or Application : How each cluster is arranged in component space can tell you which US counties are most similar and what demographic traits define that similarity; this information is most often used to inform targeted, marketing campaigns that want to appeal to a specific group of people. This cluster information is also useful for learning more about a population by revealing patterns between regions that you otherwise may not have noticed

