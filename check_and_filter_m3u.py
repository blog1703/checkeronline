import requests

def check_and_filter_m3u(m3u_url, output_file='working_playlist.m3u'):
    # Загружаем M3U-плейлист по ссылке
    response = requests.get(m3u_url)
    if response.status_code != 200:
        print(f"Ошибка: Не удалось загрузить плейлист. Код статуса: {response.status_code}")
        return

    lines = response.text.splitlines()
    working_lines = []

    # Проверяем каждую строку
    for line in lines:
        if line.startswith('http'):  # Проверяем только ссылки
            try:
                # Проверяем доступность канала
                channel_response = requests.get(line, timeout=5)
                if channel_response.status_code == 200:
                    print(f"Рабочий канал: {line}")
                    working_lines.append(line)
                else:
                    print(f"Нерабочий канал: {line}")
            except Exception as e:
                print(f"Ошибка при проверке {line}: {e}")
        else:
            # Сохраняем заголовки и другие данные
            working_lines.append(line)

    # Записываем рабочие каналы в новый файл
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(working_lines))
    print(f"Рабочие каналы сохранены в файл: {output_file}")

if __name__ == "__main__":
    # Укажите ссылку на ваш M3U-плейлист
    m3u_url = "http://dmitry-tv.ddns.net/iptv/freesat/gtmedia/Playlist-01/custom_url.m3u"
    check_and_filter_m3u(m3u_url)
