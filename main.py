from Sheller import Sheller
from Querer import Querer
import json

"https://access.redhat.com/hydra/rest/securitydata/cve.json"

if __name__ == '__main__':
    cve_pages = 5
    q = Querer("red_hat", "https://access.redhat.com/hydra/rest/securitydata")
    s = Sheller("0544748797\n")
    cve_json_file_suffix = '_cve_data.json'
    reload = -1
    while reload not in ('Y', 'y', 'N', 'n'):
        reload = input("Do you want to update CVE file? (Y/N)")

    if reload in ('Y', 'y'):
        with open(q.get_name() + cve_json_file_suffix, "w+") as file:
            file.write("[")
            for i in range(1, cve_pages):
                text = q.get_with_params({"page": i}, "cve.json")
                text = text.decode("utf-8")
                text = text[1:-1]
                text += ","
                file.write(text)
            file.write("]")
            file.close()

    with open(q.get_name() + cve_json_file_suffix, "r") as file:
        arr = json.loads(file.read())

    my_d = s.run_shell_command("dpkg-query  --show", ["package_name", "version"])

    for app in my_d:
        for cve in arr:
            try:
                if app["package_name"] in cve["affected_packages"]:
                    print(app["package_name"] + " - " + cve["CVE"])

            except TypeError:
                print("ERROR")
                print(app)
                print(cve)
