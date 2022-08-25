import pathlib
import shutil
import etherator_crawler.models as models


with open('grav_md_templates/item.md', 'rb') as f:
    md_data = f.read()


with models.engine.connect():
    webpages = models.session.query(models.HostnameClass).all()
    print(type(webpages))

    for i, row in enumerate(webpages):
        print(row.hostname)
        dest_folder = 'dump/' + row.hostname
        if i % 100000 == 0:
            print(i)
        new_dir = shutil.copytree(
            'grav_md_templates', dest_folder, dirs_exist_ok=True)

        with open(str(new_dir) + '/item.md', "w", encoding='utf-8') as fin:
            text_to_write = str(md_data.decode(
                'utf-8')).replace('{{ hostname }}', row.hostname)
            print(type(text_to_write))
            fin.write(text_to_write)
