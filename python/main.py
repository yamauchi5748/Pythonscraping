import scraping
import mongo
import yaml

class Main():
    def __init__(self):
        self.Models = []

        # 設定ファイル読み込み
        with open('config.yml') as file:
            self.config = yaml.safe_load(file.read())
        
        for target in self.config['targets'] :
            print(target);

            if target['status'] :
                model = scraping.Model(target['name'], target['root'], target['url'], target['save'], target['params'] ,target['contents'])
                self.Models.append(model)

    def run(self):
        for model in self.Models:
            contents = model.run()
            mongo.Mongo(model.target_save['ip'], model.target_save['port'], model.target_save['db_name'], model.target_save['db_table']).insert(contents)
            print(str(len(contents)) + '件入りました')

if __name__ == '__main__':

    print("start")
    main = Main()
    main.run()
    exit()