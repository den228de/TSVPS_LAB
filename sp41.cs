
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace EchoServer
{
    internal class Program
    {
        // Порт по умолчанию, если не передан через аргументы командной строки.
        private const int DefaultPort = 9900;

        // Размер буфера для приема данных от клиента.
        private const int ReceiveBufferSize = 2048;

        // Размер очереди ожидающих подключений.
        private const int Backlog = 5;

        private static void Main(string[] args)
        {
            int port = ParsePort(args, DefaultPort);

            try
            {
                // Создаем TcpListener для прослушивания всех сетевых интерфейсов на указанном порту.
                using TcpListener listener = new TcpListener(IPAddress.Any, port);

                // Настраиваем внутренний сокет TcpListener.
                // Свойство Server возвращает объект Socket, через который можно задать опции сокета.
                listener.Server.SetSocketOption(
                    SocketOptionLevel.Socket,
                    SocketOptionName.ReuseAddress,
                    true);

                // Запускаем прослушивание с очередью подключений backlog = 5.
                // Метод Start(int backlog) задает максимальное число ожидающих подключений.
                listener.Start(Backlog);

                Console.WriteLine($"[SERVER] Сервер запущен на порту {port}");
                Console.WriteLine("[SERVER] Ожидание подключений...");

                // Бесконечный цикл обработки входящих соединений.
                while (true)
                {
                    try
                    {
                        // Ожидаем подключение клиента.
                        // AcceptTcpClient() блокирует поток до тех пор, пока клиент не подключится.
                        using TcpClient client = listener.AcceptTcpClient();

                        // Получаем информацию о подключившемся клиенте.
                        if (client.Client.RemoteEndPoint is IPEndPoint remoteEndPoint)
                        {
                            Console.WriteLine(
                                $"[SERVER] Подключен клиент: {remoteEndPoint.Address}:{remoteEndPoint.Port}");
                        }
                        else
                        {
                            Console.WriteLine("[SERVER] Подключен клиент: адрес не определен");
                        }

                        // Получаем NetworkStream для чтения и записи данных.
                        using NetworkStream stream = client.GetStream();

                        byte[] buffer = new byte[ReceiveBufferSize];

                        // Читаем данные от клиента в буфер.
                        // Метод Read возвращает фактическое число прочитанных байт.
                        int bytesRead = stream.Read(buffer, 0, buffer.Length);

                        if (bytesRead > 0)
                        {
                            // Преобразуем полученные байты в строку.
                            string receivedText = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                            Console.WriteLine($"[SERVER] Получено: {receivedText}");

                            // Отправляем клиенту обратно те же данные (эхо).
                            // Метод Write записывает bytesRead байт из буфера в поток.
                            stream.Write(buffer, 0, bytesRead);
                            stream.Flush();

                            Console.WriteLine("[SERVER] Эхо-ответ отправлен клиенту");
                        }
                        else
                        {
                            Console.WriteLine("[SERVER] Данные от клиента не получены");
                        }


                        Console.WriteLine("[SERVER] Соединение с клиентом закрыто");
                    }
                    catch (SocketException ex)
                    {
                        Console.WriteLine($"[SERVER] Ошибка сокета при обработке клиента: {ex.Message}");
                    }
                    catch (ObjectDisposedException ex)
                    {
                        Console.WriteLine($"[SERVER] Объект уже освобожден: {ex.Message}");
                        break;
                    }
                    catch (InvalidOperationException ex)
                    {
                        Console.WriteLine($"[SERVER] Ошибка состояния: {ex.Message}");
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"[SERVER] Непредвиденная ошибка при обработке клиента: {ex.Message}");
                    }
                }
            }
            catch (SocketException ex)
            {
                Console.WriteLine($"[SERVER] Сетевая ошибка при запуске сервера: {ex.Message}");
            }
            catch (ArgumentOutOfRangeException ex)
            {
                Console.WriteLine($"[SERVER] Некорректный порт: {ex.Message}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[SERVER] Критическая ошибка: {ex.Message}");
            }
            finally
            {
                Console.WriteLine("[SERVER] Сервер завершил работу");
            }
        }

        // Разбираем порт из аргументов командной строки.
        // Если аргумент отсутствует или некорректен, возвращается значение по умолчанию.
        private static int ParsePort(string[] args, int defaultPort)
        {
            if (args.Length == 0)
            {
                return defaultPort;
            }

            if (int.TryParse(args[0], out int port) && port > 0 && port <= 65535)
            {
                return port;
            }

            Console.WriteLine(
                $"[SERVER] Некорректный порт \"{args[0]}\". Используется порт по умолчанию {defaultPort}");
            return defaultPort;
        }
    }
}


