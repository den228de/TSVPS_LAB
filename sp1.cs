using System;
using System.Net;
using System.Net.Sockets;

class Program
{
    static void Main()
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;

        while (true)
        {
            ShowMenu();
            Console.Write("Выберите пункт: ");
            string choice = Console.ReadLine()?.Trim() ?? "";

            Console.WriteLine();

            switch (choice)
            {
                case "1":
                    CreateIpDifferentWays();
                    break;
                case "2":
                    ShowBuiltInAddresses();
                    break;
                case "3":
                    DetermineAddressingScheme();
                    break;
                case "4":
                    WorkWithEndpoints();
                    break;
                case "0":
                    Console.WriteLine("Выход.");
                    return;
                default:
                    Console.WriteLine("Неверный пункт меню. Повторите ввод.");
                    break;
            }

            Console.WriteLine("\nНажмите Enter для продолжения...");
            Console.ReadLine();
            Console.Clear();
        }
    }

    static void ShowMenu()
    {
        Console.WriteLine("=== Работа с IP-адресами и конечными точками ===");
        Console.WriteLine("1) Создание IP-адреса разными способами");
        Console.WriteLine("2) Встроенные IP-адреса (Loopback / Any / Broadcast)");
        Console.WriteLine("3) Определение схемы адресации для введённого IP");
        Console.WriteLine("4) Создание и работа с IPEndPoint");
        Console.WriteLine("0) Выход");
        Console.WriteLine();
    }

    // -------------------- 1) Создание IPAddress разными способами --------------------
    static void CreateIpDifferentWays()
    {
        Console.WriteLine("=== 1) Создание IP-адреса разными способами ===\n");

        // 1) Через массив байтов
        Console.WriteLine("1) Через массив байтов (IPv4 пример: 192.168.1.1)");
        try
        {
            byte[] bytes = new byte[] { 192, 168, 1, 1 };
            IPAddress ipFromBytes = new IPAddress(bytes);
            Console.WriteLine($"   IP из байтов: {ipFromBytes}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   Ошибка при создании из байтов: {ex.Message}");
        }

        Console.WriteLine();

        // 2) Через значение long (для IPv4 удобно показывать на примере)
        // Важно: конструктор IPAddress(long) исторически используется, но порядок байтов может быть "неожиданным".
        // Для учебной работы оставим демонстрацию + пояснение.
        Console.WriteLine("2) Через значение long (демонстрация, возможны особенности порядка байтов)");
        try
        {
            long value = ReadLong("   Введите число (0..4294967295) для IPv4: ", 0, 4294967295);

            // Преобразуем в IPv4 безопасно через bytes (чтобы избежать путаницы порядка байтов):
            // value -> 4 байта в сетевом порядке (big-endian)
            byte[] b = new byte[4];
            b[0] = (byte)((value >> 24) & 0xFF);
            b[1] = (byte)((value >> 16) & 0xFF);
            b[2] = (byte)((value >> 8) & 0xFF);
            b[3] = (byte)(value & 0xFF);

            IPAddress ipFromLong = new IPAddress(b);
            Console.WriteLine($"   IP из long (через разбиение на байты): {ipFromLong}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   Ошибка: {ex.Message}");
        }

        Console.WriteLine();

        // 3) Parse()
        Console.WriteLine("3) Parse() — выбросит исключение при неверном вводе");
        Console.Write("   Введите IP (например 10.0.0.1 или ::1): ");
        string sParse = Console.ReadLine()?.Trim() ?? "";

        try
        {
            IPAddress ipParse = IPAddress.Parse(sParse);
            Console.WriteLine($"   Parse() успешно: {ipParse} | Family: {ipParse.AddressFamily}");
        }
        catch (FormatException)
        {
            Console.WriteLine("   Parse(): неверный формат IP-адреса (FormatException).");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   Parse(): другая ошибка: {ex.Message}");
        }

        Console.WriteLine();

        // 4) TryParse()
        Console.WriteLine("4) TryParse() — безопасная проверка без исключений");
        Console.Write("   Введите IP (например 172.16.0.5 или fe80::1): ");
        string sTry = Console.ReadLine()?.Trim() ?? "";

        if (IPAddress.TryParse(sTry, out IPAddress? ipTry))
        {
            Console.WriteLine($"   TryParse() успешно: {ipTry} | Family: {ipTry.AddressFamily}");
        }
        else
        {
            Console.WriteLine("   TryParse(): не удалось распознать IP-адрес.");
        }
    }

    // -------------------- 2) Встроенные адреса --------------------
    static void ShowBuiltInAddresses()
    {
        Console.WriteLine("=== 2) Встроенные IP-адреса ===\n");

        // Loopback: 127.0.0.1 (IPv4), есть также IPv6 Loopback: ::1
        IPAddress loopbackV4 = IPAddress.Loopback;
        IPAddress loopbackV6 = IPAddress.IPv6Loopback;

        // Any: 0.0.0.0, IPv6Any: ::
        IPAddress anyV4 = IPAddress.Any;
        IPAddress anyV6 = IPAddress.IPv6Any;

        // Broadcast: 255.255.255.255 (только IPv4)
        IPAddress broadcast = IPAddress.Broadcast;

        Console.WriteLine($"Loopback (IPv4):   {loopbackV4}");
        Console.WriteLine($"Loopback (IPv6):   {loopbackV6}");
        Console.WriteLine($"Any (IPv4):        {anyV4}");
        Console.WriteLine($"Any (IPv6):        {anyV6}");
        Console.WriteLine($"Broadcast (IPv4):  {broadcast}");

        Console.WriteLine("\nПримечание:");
        Console.WriteLine("- Loopback используется для обращения к самому себе.");
        Console.WriteLine("- Any означает \"слушать на всех интерфейсах\" (bind).");
        Console.WriteLine("- Broadcast — широковещательный IPv4 адрес.");
    }

    // -------------------- 3) Схема адресации --------------------
    static void DetermineAddressingScheme()
    {
        Console.WriteLine("=== 3) Определение схемы адресации ===\n");
        IPAddress ip = ReadIPAddress("Введите IP-адрес (IPv4/IPv6): ");

        Console.WriteLine($"\nIP: {ip}");
        Console.WriteLine($"AddressFamily: {ip.AddressFamily}");

        // Для IPv4: определим класс адресации по первому октету (классическая схема A/B/C/D/E)
        if (ip.AddressFamily == AddressFamily.InterNetwork)
        {
            byte[] bytes = ip.GetAddressBytes();
            byte first = bytes[0];

            string ipClass =
                (first >= 1 && first <= 126) ? "A" :
                (first >= 128 && first <= 191) ? "B" :
                (first >= 192 && first <= 223) ? "C" :
                (first >= 224 && first <= 239) ? "D (Multicast)" :
                (first >= 240 && first <= 254) ? "E (Experimental)" :
                (first == 127) ? "Loopback (127.0.0.0/8)" :
                (first == 0) ? "0.0.0.0/8 (спец. диапазон)" :
                "Не определено";

            Console.WriteLine($"Класс (IPv4): {ipClass}");

            // Доп. “схема” (частный/публичный) — полезно для практики
            bool isPrivate =
                (first == 10) ||
                (first == 172 && bytes[1] >= 16 && bytes[1] <= 31) ||
                (first == 192 && bytes[1] == 168);

            Console.WriteLine($"Тип: {(isPrivate ? "Частный (Private)" : "Публичный/прочий")}");
        }
        else
        {
            // Для IPv6 "классы" A/B/C не применяются
            Console.WriteLine("Для IPv6 классическая классовая адресация A/B/C не используется.");

            // Можем показать базовую категоризацию по типичным префиксам (упрощённо, учебно)
            string s = ip.ToString().ToLowerInvariant();

            if (IPAddress.IsLoopback(ip))
                Console.WriteLine("Категория (IPv6): Loopback (::1)");
            else if (s.StartsWith("fe80:"))
                Console.WriteLine("Категория (IPv6): Link-local (fe80::/10)");
            else if (s.StartsWith("fc") || s.StartsWith("fd"))
                Console.WriteLine("Категория (IPv6): Unique local (fc00::/7)");
            else if (s.StartsWith("ff"))
                Console.WriteLine("Категория (IPv6): Multicast (ff00::/8)");
            else
                Console.WriteLine("Категория (IPv6): Глобальный/прочий (упрощённо).");
        }
    }

    // -------------------- 4) Работа с IPEndPoint --------------------
    static void WorkWithEndpoints()
    {
        Console.WriteLine("=== 4) Создание и работа с IPEndPoint ===\n");

        Console.WriteLine("1) Создать IPEndPoint через IPAddress и порт");
        IPAddress ip = ReadIPAddress("   Введите IP: ");
        int port = ReadInt("   Введите порт (1..65535): ", 1, 65535);

        IPEndPoint ep1 = new IPEndPoint(ip, port);
        PrintEndpointInfo("   EndPoint #1", ep1);

        Console.WriteLine();

        Console.WriteLine("2) Создать через строку в формате \"адрес:порт\"");
        Console.WriteLine("   Примеры: 192.168.1.10:8080");
        Console.WriteLine("   Для IPv6 используйте скобки: [fe80::1]:443");
        Console.Write("   Введите строку: ");
        string input = Console.ReadLine()?.Trim() ?? "";

        if (TryParseEndPoint(input, out IPEndPoint? ep2, out string error))
        {
            PrintEndpointInfo("   EndPoint #2", ep2!);
        }
        else
        {
            Console.WriteLine($"   Ошибка разбора конечной точки: {error}");
        }
    }

    static void PrintEndpointInfo(string title, IPEndPoint ep)
    {
        Console.WriteLine($"{title}: {ep}");
        Console.WriteLine($"      Address: {ep.Address}");
        Console.WriteLine($"      Port:    {ep.Port}");
        Console.WriteLine($"      Family:  {ep.AddressFamily}");
    }

    // Парсинг "address:port" с поддержкой IPv6 в [ ]
    static bool TryParseEndPoint(string input, out IPEndPoint? endpoint, out string error)
    {
        endpoint = null;
        error = "";

        if (string.IsNullOrWhiteSpace(input))
        {
            error = "Пустая строка.";
            return false;
        }

        string addressPart;
        string portPart;

        // IPv6 в формате [addr]:port
        if (input.StartsWith("["))
        {
            int closing = input.IndexOf(']');
            if (closing < 0)
            {
                error = "Для IPv6 ожидается закрывающая скобка ']'.";
                return false;
            }

            addressPart = input.Substring(1, closing - 1);

            if (closing + 1 >= input.Length || input[closing + 1] != ':')
            {
                error = "После ']' ожидается ':' и порт.";
                return false;
            }

            portPart = input.Substring(closing + 2);
        }
        else
        {
            // IPv4 (или хост без двоеточий) "addr:port"
            // Важно: IPv6 без скобок тут не поддерживаем специально, чтобы не путать двоеточия IPv6 с разделителем.
            int idx = input.LastIndexOf(':');
            if (idx <= 0 || idx == input.Length - 1)
            {
                error = "Ожидается формат address:port (например 192.168.1.1:80) или [IPv6]:port.";
                return false;
            }

            addressPart = input.Substring(0, idx);
            portPart = input.Substring(idx + 1);
        }

        if (!IPAddress.TryParse(addressPart, out IPAddress? ip))
        {
            error = $"Неверный IP-адрес: '{addressPart}'.";
            return false;
        }

        if (!int.TryParse(portPart, out int port) || port < 1 || port > 65535)
        {
            error = $"Неверный порт: '{portPart}'. Допустимо 1..65535.";
            return false;
        }

        endpoint = new IPEndPoint(ip, port);
        return true;
    }

    // -------------------- Вспомогательные функции ввода/валидации --------------------
    static IPAddress ReadIPAddress(string prompt)
    {
        while (true)
        {
            Console.Write(prompt);
            string s = Console.ReadLine()?.Trim() ?? "";

            if (IPAddress.TryParse(s, out IPAddress? ip))
                return ip;

            Console.WriteLine("Неверный IP-адрес. Повторите ввод.\n");
        }
    }

    static int ReadInt(string prompt, int min, int max)
    {
        while (true)
        {
            Console.Write(prompt);
            string s = Console.ReadLine()?.Trim() ?? "";

            if (int.TryParse(s, out int value) && value >= min && value <= max)
                return value;

            Console.WriteLine($"Ошибка ввода. Введите целое число от {min} до {max}.\n");
        }
    }

    static long ReadLong(string prompt, long min, long max)
    {
        while (true)
        {
            Console.Write(prompt);
            string s = Console.ReadLine()?.Trim() ?? "";

            if (long.TryParse(s, out long value) && value >= min && value <= max)
                return value;

            Console.WriteLine($"Ошибка ввода. Введите число от {min} до {max}.\n");
        }
    }
}
