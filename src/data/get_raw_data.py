import os
from dotenv import load_dotenv, find_dotenv
from requests import Session
import logging

#payload for post
payload = {
    'action': 'login',
    'username': os.environ.get("KAGGAL_USERNAME"),
    'password': os.environ.get("KAGGAL_PASSWORD")
}

def extract_data(url, file_path):
    '''
    Extract data from kaggle
    '''
    with Session() as c:
        c.post('https://www.kaggle.com/account/login?phase=emailSignIn&returnUrl=%2F', data=payload)
        with open(file_path, 'w') as handle:
            response = c.get(url, stream=True)
            for block in response.iter_content(1024):
                handle.write(block)

def main(project_dir):
    '''
    main method
    '''
    #get logging
    logger = logging.getLogger(__name__)
    logger.info('getting raw data')
    
    #urls 
    url_train = 'https://www.kaggle.com/c/titanic/download/GQf0y8ebHO0C4JXscPPp%2Fversions%2FXkNkvXwqPPVG0Qt3MtQT%2Ffiles%2Ftrain.csv'
    url_test = 'https://www.kaggle.com/c/titanic/download/GQf0y8ebHO0C4JXscPPp%2Fversions%2FXkNkvXwqPPVG0Qt3MtQT%2Ffiles%2Ftest.csv'

    #file paths
    raw_data_path = os.path.join(os.path.pardir,'data','raw')
    train_data_path = os.path.join(raw_data_path,'train.csv')
    test_data_path = os.path.join(raw_data_path,'test.csv')
    
    #extract data
    extract_data(url_train, train_data_path)
    extract_data(url_test, test_data_path)
    logging.info('downloading raw training and test data')

if __name__ == '__main__':
    #getting root dir 
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    print(__file__)
    print(__name__)
    #print(__main__)
    
    #setup logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    
    #find .env 
    dotenv_path = find_dotenv()
    #load .env
    load_dotenv(dotenv_path)
    
    #call the main
    main(project_dir)
    