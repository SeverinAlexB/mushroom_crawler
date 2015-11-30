import re, os, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import StringIO
from PIL import Image
from pattern.web import URL, DOM
import multiprocessing as mp
 
class GoogleImageExtractor(object):

    @classmethod
    def from_keyword(cls, keyword, target_folder, nb_images):
        extractor = cls()
        extractor.keyword = keyword
        extractor.nb_images = nb_images
        extractor.target_folder = target_folder
        return extractor
 
    def __init__(self):
        """ Google image search class
            Args:
                search_key to be entered.
 
        """
        self.keyword = ''
        self.formated_keyword = ''
        self.target_folder = ''
        self.nb_images = 200
 
        ## url construct string text
        self.prefix_of_search_url = "https://www.google.com.sg/search?q="
        self.postfix_of_search_url = '&source=lnms&tbm=isch&sa=X&ei=0eZEVbj3IJG5uATalICQAQ&ved=0CAcQ_AUoAQ&biw=939&bih=591'# non changable text
        self.target_url_str = ''
        self.pic_url_list = []
        self.nb_threads = 30


    def formed_search_url(self):
        formated_keyword = self.keyword.rstrip().replace(' ', '+')
        return self.prefix_of_search_url + formated_keyword +\
                                self.postfix_of_search_url
 
    def retrieve_source_fr_html(self, google_search_url):
        """ Make use of selenium. Retrieve from html table using pandas table.
 
        """
        driver = webdriver.Firefox()
        driver.get(google_search_url)
        delay = 5 #sec
        ## wait for log in then get the page source.
        try:
            driver.execute_script("window.scrollTo(0, 30000)")
            time.sleep(delay)
            self.temp_page_source = driver.page_source
            driver.find_element_by_id('smb').click() #ok

            nb_scroll = 3
            for i in range(nb_scroll):
                time.sleep(delay)
                driver.execute_script("window.scrollTo(0, 60000)")

 
        except:
            print 'not able to find'
            driver.quit()
        self.page_source = driver.page_source
 
        driver.close()
 
    def extract_pic_url(self):
        """ extract all the raw pic url in list
 
        """
        dom = DOM(self.page_source)
        tag_list = dom('a.rg_l')
        print len(tag_list)
        for tag in tag_list[:self.nb_images]:
            tar_str = re.search('imgurl=(.*)&imgrefurl', tag.attributes['href'])
            try:
                self.pic_url_list.append(tar_str.group(1))
            except:
                print 'error parsing', tag
 
    def multi_search_download(self):
        google_search_url = self.formed_search_url()
        self.retrieve_source_fr_html(google_search_url)
        self.extract_pic_url()

        #target_folder = self.folder_main_dir_prefix + "/" + self.g_search_key
        self.downloading_all_photos() #some download might not be jpg?? use selnium to download??

    def downloading_all_photos(self):
        """ download all photos to particular folder
 
        """
        download_list = []
        self.create_folder(self.target_folder)
        pic_counter = 1
        for url_link in self.pic_url_list:
            pic_prefix_str = self.keyword + str(pic_counter)
            param = (url_link.encode(), pic_prefix_str, self.target_folder)
            download_list.append(param)
            pic_counter = pic_counter +1

        print "Download " + str(pic_counter) + " images"

        self.run_async(download_list)

    def run_async(self, downloadlist):
        pool = mp.Pool(processes=self.nb_threads)
        pool.map(_download_single_image, downloadlist)
        pool.close()
        pool.join()

    def create_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

def _download_single_image(args):
    try:
        download_single_image(*args)
    except Exception as e:
        print str(e)


def download_single_image(url_link, pic_prefix_str, target_folder):
    """ Download data according to the url link given.
        Args:
            url_link (str): url str.
            pic_prefix_str (str): pic_prefix_str for unique label the pic
    """
    file_ext = os.path.splitext(url_link)[1] #use for checking valid pic ext
    temp_filename = pic_prefix_str + ".jpg"
    temp_filename_full_path = os.path.join(target_folder, temp_filename)

    valid_image_ext_list = ['.png','.jpg','.jpeg', '.gif', '.bmp', '.tiff'] #not comprehensive

    url = URL(url_link)
    if url.redirect:
        return # if there is re-direct, return

    if file_ext not in valid_image_ext_list:
        return #return if not valid image extension

     # save as test.gif
    print url_link
    try:
        response = url.download()
        img = resize_image(response)
        img.save(temp_filename_full_path, "JPEG")
    except Exception as e:
        #if self.__print_download_fault:
        print 'Problem with processing this data: ', str(e), url_link

def resize_image(response):
        size = (300,300)
        buff = StringIO.StringIO(response)
        img = Image.open(buff)
        img.thumbnail(size, Image.ANTIALIAS)
        return img

 
if __name__ == '__main__':
        w = GoogleImageExtractor('fly agaric')
        w.multi_search_download()