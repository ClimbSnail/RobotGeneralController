import json
import codecs
import massagehead as mh

class Language(object):
    def __init__(self, path):
        """
        多语言管理类初始化
        :param path: 语言文件所在目录
        """
        self.language_path = path
        self.language_setting = None    # 默认语言设置
        self.language_key = None    # 保存各个语种信息
        self.word_set = None    # 程序所涉及的所有词组信息
        self.language = None    # self.language_setting对应的所有词组文字
        self.read_langueage(self.language_path)

    def read_langueage(self, read_path):
        """
        读取语言信息
        :param read_path: 语言文件所在的路径
        :return: None
        """
        fp = codecs.open(read_path, "r", "utf8")
        self.set_data = json.load(fp)
        fp.close()

        self.language_setting = self.set_data["language_set"].strip()
        self.language_key = self.set_data["language_key"]
        self.word_set = self.set_data["word_set"]
        self.language = self.set_data["language"]
        # 获取支持的语种信息，存放在list中
        self.language_key_list = [ key for key in self.language_key.split(", ") ]

    def get_data(self, language = None):
        """
        获取设定语种所对应的所有词组信息
        :param language: 语种类别
        :return: 所有语种信息 词组对应关系map
        """
        language = self.language_setting if language == None else language
        if language in self.language_key_list:
            # 保存到语言文件中
            self.language_setting = language
            self.save_language(self.language_path)
            # 获取对应语言的文字
            word_keys = self.word_set.keys()
            word_map_map = {}
            for word_key in word_keys:
                word_key_map = self.word_set[word_key].split(", ")
                word_val_map = self.language[language][word_key].split(", ")
                word_map_map[word_key] = { key:val for key, val in zip(word_key_map, word_val_map) }
            return self.language_key_list, word_map_map
        else:
            print("error")
            return None, None

    def save_language(self, save_path):
        """
        保存配置，并写入文件
        :param save_path:写入目标文件的路径
        :return:None
        """
        fp = codecs.open(save_path, "w", "utf8")
        w_data = {
            "language_set": self.language_setting,
            "language_key": self.language_key,
            "word_set": self.word_set,
            "language": self.language
        }
        json.dump(w_data, fp, indent=2)
        fp.close()

    def api(self, action, param = None):
        """
        供给外部调用的api
        :param action:请求动作
        :param param:携带的参数
        """
        if action == mh.A_UPDATALANG:   # 语言更新
            return self.get_data(param)

class ModelFile(object):
    def __init__(self):
        self.file_path = None
        pass

    def create_file(self, file_path):
        self.file_path = file_path
        fp = codecs.open(self.file_path, "w", "utf8")
        json.dump({}, fp, indent=2)
        fp.close()

    def read(self, file_path):
        """
        读取模型信息
        :param read_path: 模型文件所在的路径
        :return: 模型各组件的位置信息
        """
        self.file_path = file_path
        fp = codecs.open(self.file_path, "r", "utf8")
        self.model_data = json.load(fp)
        fp.close()
        # 得到所有的模型组件名称
        name_list = self.model_data["model_name_list"].strip().split()
        model_info = {}
        for name in name_list:
            key = name.strip()
            model_info[key] = self.model_data[key]
        return model_info

    def save(self, model_info, save_path=None):
        """
        保存模型文件
        :param save_path:写入目标文件的路径
        :param model_info:模型相关的数据
        :return:None
        """
        if save_path!=None:
            self.file_path = save_path
        names = [ name.strip() for name in model_info.keys()]
        model_name = ""
        for name in names:
            model_name = model_name+" "+name
        w_data = {
            "model_name_list":model_name.strip(),
        }
        for key, info in model_info.items():
            w_data[key] = info
        fp = codecs.open(self.file_path, "w", "utf8")
        json.dump(w_data, fp, indent=2)
        fp.close()

    def __del__(self):
        pass

class ActionFile(object):
    def __init__(self):
        pass

    def create_file(self, file_path):
        self.file_path = file_path
        fp = codecs.open(self.file_path, "w", "utf8")
        json.dump({}, fp, indent=2)
        fp.close()

    def read(self, file_path):
        """
        读取模型信息
        :param read_path: 动作组文件所在的路径
        :return: 动作组信息
        """
        self.file_path = file_path
        fp = codecs.open(self.file_path, "r", "utf8")
        self.action_data = json.load(fp)
        fp.close()
        # 得到所有的模型组件名称
        num_list = self.action_data["model_num_list"].strip().split()
        action_info = {}
        for num in num_list:
            key = num.strip()
            action_info[key] = self.action_data[key]
        return action_info

    def save(self, action_info, save_path=None):
        """
        保存模型文件
        :param save_path:写入目标文件的路径
        :param model_info:模型相关的数据
        :return:None
        """
        if save_path!=None:
            self.file_path = save_path
        names = [ name.strip() for name in action_info.keys()]
        action_num = ""
        for name in names:
            action_num = action_num+" "+name
        w_data = {
            "action_num_list":action_num.strip(),
        }
        for key, info in action_info.items():
            w_data[key] = info
        fp = codecs.open(self.file_path, "w", "utf8")
        json.dump(w_data, fp, indent=2)
        fp.close()

    def __del__(self):
        pass

class SystemConfig(object):
    """
    系统配置文件类
    """
    def __init__(self, filepath):
        """
        系统配置文件类初始化
        :param filepath: 配置文件所在目录
        """
        self.cfgfile_path = filepath
        self.m_sysinfo = {}
        self.read()

    def read(self):
        """
        读取系统配置信息
        :return: 系统配置信息
        """
        fp = codecs.open(self.cfgfile_path, "r", "utf8")
        self.m_sysinfo = json.load(fp)
        fp.close()
        return self.m_sysinfo

    def api(self, action, param):
        if action == None:
            pass

    def __del__(self):
        pass

if __name__ == "__main__":
    lang = Language("./language")  # first
    print(lang["language_set"])