from JenkinsClustering import JenkinsClustering
from sklearn.cluster import KMeans
from Statistics import Statistics
import json
import traceback

def do_clustering():
    try:
        j = JenkinsClustering()
        # get the data and dataframe to perform clustering
        data, df = j.prepare_data_for_clustering()
        print('Proceeding to cluster the data')
        estimator = KMeans(n_clusters=30, init = 'k-means++', max_iter = 1000)
        estimator.fit(data)
        print(estimator.labels_)

        df['labels'] = estimator.labels_

        for item in set(estimator.labels_):
            con_string = ''
            for i in range(len(df)):
                if df['labels'][i] == item:
                    con_string += df['text'][i]
            Statistics.create_word_cloud(con_string, "Cluster %s" %(item), '/Users/sandeepjoshi/Documents/CS540/Course_Project/sandeep_joshi__debojit_kaushik_course_project/cluster_%s.png' %(item))
            print('Created the word cloud for the cluster: ' + item )
    
    except Exception:
        print('Error performing clustering')
    

def get_statistics():
    try:
        s = Statistics()
        path = "./Jenkinsfiles/"
        s.get_timeout_stats(path)
        s.build_tool_stats(path)
        s.build_word_cloud_high_level(path)
        s.build_word_cloud_low_level(path)
        s.get_trigger_statistics()
        s.consolidate_post_block_statistics()
        s.get_post_block_correlation_statistics()
        s.get_parallel_block_statistics()
        with open('results.json','w',encoding='utf8') as f:
            f.write(json.dumps(s.statistics_dict, ensure_ascii=False))    
    except Exception:
        traceback.format_exc()
    

if __name__ == '__main__':
    try:
        get_statistics()
        do_clustering()
    except Exception:
        traceback.format_exc()