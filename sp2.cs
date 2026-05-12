using System;
using System.IO;
using System.Linq;
using System.Net.NetworkInformation;
using System.Text;

internal static class Program
{
    private static string _lastReport = "";

    static void Main()
    {
        Console.OutputEncoding = Encoding.UTF8;
        Console.WriteLine("Монитор сетевой активности");

        bool exit = false;
        while (!exit)
        {
            ShowMenu();
            string? choice = Console.ReadLine();

            try
            {
                switch (choice)
                {
                    case "1":
                        _lastReport = BuildInterfacesReport();
                        PrintReport(_lastReport);
                        Pause();
                        break;

                    case "2":
                        _lastReport = BuildTcpReport();
                        PrintReport(_lastReport);
                        Pause();
                        break;

                    case "3":
                        _lastReport = BuildGlobalNetworkStatsReport();
                        PrintReport(_lastReport);
                        Pause();
                        break;

                    case "4":
                        SaveLastReportToFile();
                        Pause();
                        break;

                    case "5":
                        exit = true;
                        break;

                    default:
                        Console.WriteLine("Неверный выбор.");
                        Pause();
                        break;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Ошибка при получении/обработке данных:");
                Console.WriteLine(ex.Message);
                Pause();
            }
        }
    }

    private static void ShowMenu()
    {
        Console.Clear();
        Console.WriteLine("Выберите действие:");
        Console.WriteLine("1. Просмотреть сетевые интерфейсы");
        Console.WriteLine("2. Показать TCP-подключения");
        Console.WriteLine("3. Статистика сети (IPv4/IPv6 глобальная)");
        Console.WriteLine("4. Сохранить последний отчёт в файл (опционально)");
        Console.WriteLine("5. Выход");
        Console.Write("Ваш выбор: ");
    }

    private static void PrintReport(string report)
    {
        Console.Clear();
        Console.WriteLine(report);
    }

    private static void Pause()
    {
        Console.WriteLine();
        Console.Write("Нажмите Enter, чтобы продолжить...");
        Console.ReadLine();
    }

    // 1) Мониторинг интерфейсов + статистика
    private static string BuildInterfacesReport()
    {
        var sb = new StringBuilder();
        sb.AppendLine("=== Сетевые интерфейсы ===");
        sb.AppendLine($"Время: {DateTime.Now:yyyy-MM-dd HH:mm:ss}");
        sb.AppendLine();

        NetworkInterface[] nics = NetworkInterface.GetAllNetworkInterfaces();
        if (nics.Length == 0)
        {
            sb.AppendLine("Сетевые интерфейсы не найдены.");
            return sb.ToString();
        }

        foreach (var ni in nics.OrderBy(x => x.Name))
        {
            sb.AppendLine(new string('-', 90));
            sb.AppendLine($"Имя:            {ni.Name}");
            sb.AppendLine($"Описание:       {ni.Description}");
            sb.AppendLine($"ID:             {ni.Id}");
            sb.AppendLine($"Тип:            {ni.NetworkInterfaceType}");
            sb.AppendLine($"Статус:         {ni.OperationalStatus}");
            sb.AppendLine($"Скорость:       {FormatSpeed(ni.Speed)}");
            sb.AppendLine($"MAC:            {FormatMac(ni.GetPhysicalAddress())}");
            sb.AppendLine($"DNS включён:    {ni.GetIPProperties().IsDnsEnabled}");
            sb.AppendLine($"Dynamic DNS:    {ni.GetIPProperties().IsDynamicDnsEnabled}");

            try
            {
                var stats = ni.GetIPStatistics();
                sb.AppendLine();
                sb.AppendLine("  [Статистика интерфейса]");
                sb.AppendLine($"  Bytes Received:              {stats.BytesReceived:n0}");
                sb.AppendLine($"  Bytes Sent:                  {stats.BytesSent:n0}");

                long totalPacketsIn = stats.UnicastPacketsReceived + stats.NonUnicastPacketsReceived;
                long totalPacketsOut = stats.UnicastPacketsSent + stats.NonUnicastPacketsSent;

                sb.AppendLine($"  Packets Received (total):    {totalPacketsIn:n0}");
                sb.AppendLine($"    Unicast Received:          {stats.UnicastPacketsReceived:n0}");
                sb.AppendLine($"    Non-Unicast Received:      {stats.NonUnicastPacketsReceived:n0}");

                sb.AppendLine($"  Packets Sent (total):        {totalPacketsOut:n0}");
                sb.AppendLine($"    Unicast Sent:              {stats.UnicastPacketsSent:n0}");
                sb.AppendLine($"    Non-Unicast Sent:          {stats.NonUnicastPacketsSent:n0}");

                sb.AppendLine($"  Incoming Discarded:          {stats.IncomingPacketsDiscarded:n0}");
                sb.AppendLine($"  Incoming Errors:             {stats.IncomingPacketsWithErrors:n0}");
                sb.AppendLine($"  Outgoing Discarded:          {stats.OutgoingPacketsDiscarded:n0}");
                sb.AppendLine($"  Outgoing Errors:             {stats.OutgoingPacketsWithErrors:n0}");
                sb.AppendLine($"  Output Queue Length:         {stats.OutputQueueLength:n0}");
            }
            catch (Exception ex)
            {
                sb.AppendLine();
                sb.AppendLine("  [Статистика интерфейса недоступна]");
                sb.AppendLine($"  Причина: {ex.Message}");
            }
        }

        sb.AppendLine(new string('-', 90));
        return sb.ToString();
    }

    // 2) Анализ TCP-подключений
    private static string BuildTcpReport()
    {
        var sb = new StringBuilder();
        sb.AppendLine("=== Активные TCP-соединения ===");
        sb.AppendLine($"Время: {DateTime.Now:yyyy-MM-dd HH:mm:ss}");
        sb.AppendLine();

        IPGlobalProperties ipProps = IPGlobalProperties.GetIPGlobalProperties();

        TcpConnectionInformation[] conns;
        try
        {
            conns = ipProps.GetActiveTcpConnections();
        }
        catch (Exception ex)
        {
            sb.AppendLine("Не удалось получить список TCP-соединений.");
            sb.AppendLine(ex.Message);
            return sb.ToString();
        }

        if (conns.Length == 0)
        {
            sb.AppendLine("Активных TCP-соединений нет.");
            return sb.ToString();
        }

        sb.AppendLine($"Всего: {conns.Length}");
        sb.AppendLine();
        sb.AppendLine($"{Pad("Local", 30)} {Pad("Remote", 30)} State");
        sb.AppendLine(new string('-', 80));

        foreach (var c in conns.OrderBy(x => x.State).ThenBy(x => x.LocalEndPoint.ToString()))
        {
            string local = $"{c.LocalEndPoint.Address}:{c.LocalEndPoint.Port}";
            string remote = $"{c.RemoteEndPoint.Address}:{c.RemoteEndPoint.Port}";
            sb.AppendLine($"{Pad(local, 30)} {Pad(remote, 30)} {c.State}");
        }

        return sb.ToString();
    }

    // 3) Сбор сетевой статистики (общая)
    private static string BuildGlobalNetworkStatsReport()
    {
        var sb = new StringBuilder();
        sb.AppendLine("=== Глобальная статистика сети (IPGlobalProperties) ===");
        sb.AppendLine($"Время: {DateTime.Now:yyyy-MM-dd HH:mm:ss}");
        sb.AppendLine();

        IPGlobalProperties props = IPGlobalProperties.GetIPGlobalProperties();

        try
        {
            var v4 = props.GetIPv4GlobalStatistics();
            sb.AppendLine("[IPv4]");
            AppendGlobalStats(sb, v4);
            sb.AppendLine();
        }
        catch (Exception ex)
        {
            sb.AppendLine("[IPv4] Недоступно: " + ex.Message);
            sb.AppendLine();
        }

        try
        {
            var v6 = props.GetIPv6GlobalStatistics();
            sb.AppendLine("[IPv6]");
            AppendGlobalStats(sb, v6);
            sb.AppendLine();
        }
        catch (Exception ex)
        {
            sb.AppendLine("[IPv6] Недоступно: " + ex.Message);
            sb.AppendLine();
        }

        sb.AppendLine("Примечание: 'ошибки фрагментации/реассемблирования' зависят от поддержки ОС и версии .NET.");
        return sb.ToString();
    }

    private static void AppendGlobalStats(StringBuilder sb, IPGlobalStatistics s)
    {
        // Пакеты: общее/доставленные/сброшенные и т.п.
        sb.AppendLine($"  ReceivedPackets:                 {TryGetLong(s, "ReceivedPackets"):n0}");
        sb.AppendLine($"  ReceivedPacketsDelivered:        {TryGetLong(s, "ReceivedPacketsDelivered"):n0}");
        sb.AppendLine($"  ReceivedPacketsDiscarded:        {TryGetLong(s, "ReceivedPacketsDiscarded"):n0}");
        sb.AppendLine($"  ReceivedPacketsForwarded:        {TryGetLong(s, "ReceivedPacketsForwarded"):n0}");

        sb.AppendLine($"  OutputPacketRequests:            {TryGetLong(s, "OutputPacketRequests"):n0}");
        sb.AppendLine($"  OutputPacketsDiscarded:          {TryGetLong(s, "OutputPacketsDiscarded"):n0}");
        sb.AppendLine($"  OutputPacketsNoRoute:            {TryGetLong(s, "OutputPacketsWithNoRoute"):n0}");

        // Ошибки (заголовки/адреса/неизвестные протоколы)
        sb.AppendLine($"  HeaderErrors:                    {TryGetLong(s, "ReceivedPacketsWithHeadersErrors"):n0}");
        sb.AppendLine($"  AddressErrors:                   {TryGetLong(s, "ReceivedPacketsWithAddressErrors"):n0}");
        sb.AppendLine($"  UnknownProtocol:                 {TryGetLong(s, "ReceivedPacketsWithUnknownProtocol"):n0}");

        // Фрагментация / реассемблирование (если поля есть — выведутся, иначе будет -1)
        sb.AppendLine($"  PacketsFragmented:               {TryGetLong(s, "PacketsFragmented"):n0}");
        sb.AppendLine($"  PacketFragmentFailures:          {TryGetLong(s, "PacketFragmentFailures"):n0}");
        sb.AppendLine($"  PacketFragmentsCreated:          {TryGetLong(s, "PacketFragmentsCreated"):n0}");

        sb.AppendLine($"  PacketReassemblyRequired:        {TryGetLong(s, "PacketReassemblyRequired"):n0}");
        sb.AppendLine($"  PacketReassemblyFailures:        {TryGetLong(s, "PacketReassemblyFailures"):n0}");
        sb.AppendLine($"  PacketReassemblyTimeout:         {TryGetLong(s, "PacketReassemblyTimeout"):n0}");
    }

    // ---------- Вспомогательное ----------

    private static void SaveLastReportToFile()
    {
        if (string.IsNullOrWhiteSpace(_lastReport))
        {
            Console.WriteLine("Пока нечего сохранять. Сначала выполните пункт 1/2/3.");
            return;
        }

        string fileName = $"network_report_{DateTime.Now:yyyyMMdd_HHmmss}.txt";
        File.WriteAllText(fileName, _lastReport, Encoding.UTF8);
        Console.WriteLine($"Отчёт сохранён: {Path.GetFullPath(fileName)}");
    }

    private static string Pad(string s, int width)
        => s.Length >= width ? s.Substring(0, width - 1) + "…" : s.PadRight(width);

    private static string FormatSpeed(long bitsPerSecond)
    {
        if (bitsPerSecond <= 0) return "n/a";
        double bps = bitsPerSecond;
        double mbps = bps / 1_000_000.0;
        double gbps = bps / 1_000_000_000.0;
        return gbps >= 1 ? $"{gbps:F2} Gbps" : $"{mbps:F2} Mbps";
    }

    private static string FormatMac(PhysicalAddress pa)
    {
        byte[] bytes = pa.GetAddressBytes();
        if (bytes.Length == 0) return "n/a";
        return string.Join("-", bytes.Select(b => b.ToString("X2")));
    }

    // Безопасное чтение свойств IPGlobalStatistics: если в этой ОС/.NET нет поля — вернём -1
    private static long TryGetLong(IPGlobalStatistics obj, string propName)
    {
        var p = obj.GetType().GetProperty(propName);
        if (p == null) return -1;
        object? value = p.GetValue(obj);
        if (value == null) return -1;
        try { return Convert.ToInt64(value); }
        catch { return -1; }
    }
}
