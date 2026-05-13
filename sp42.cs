
using System;
using System.Net.Sockets;
using System.Text;

namespace EchoClient
{
    internal class Program
    {
        // Порт по умолчанию, если не передан через аргументы командной строки.
        private const int DefaultPort = 9900;

        // Размер одной порции чтения ответа от сервера.
        private const int ReceiveChunkSize = 16;

        // Тестовое сообщение, которое отправляется серверу.
        private const string TestMessage = "Test message. This will be echoed";

        private static void Main(string[] args)
        {
            int port = ParsePort(args, DefaultPort);

            try
            {
                // Создаем TCP-клиент для подключения к серверу.
                using TcpClient client = new TcpClient();

                Console.WriteLine($"[CLIENT] Подключение к localhost:{port}...");

                // Подключаемся к серверу на localhost и указанном порту.
                client.Connect("localhost", port);

                Console.WriteLine("[CLIENT] Соединение установлено");

                // Получаем сетевой поток для обмена данными.
                using NetworkStream stream = client.GetStream();

                // Кодируем тестовое сообщение в массив байт.
                byte[] messageBytes = Encoding.UTF8.GetBytes(TestMessage);

                // Отправляем сообщение серверу.
                // Метод Write записывает весь массив байт в NetworkStream.
                stream.Write(messageBytes, 0, messageBytes.Length);
                stream.Flush();

                Console.WriteLine($"[CLIENT] Отправлено: {TestMessage}");

                // Сообщаем серверу, что клиент закончил отправку данных.
                // Это помогает серверу корректно завершить чтение.
                client.Client.Shutdown(SocketShutdown.Send);

                byte[] buffer = new byte[ReceiveChunkSize];
                StringBuilder responseBuilder = new StringBuilder();

                // Читаем ответ от сервера порциями по 16 байт,
                // пока сервер не закроет соединение.
                while (true)
                {
                    int bytesRead = stream.Read(buffer, 0, buffer.Length);

                    // Если Read вернул 0, значит удаленная сторона закрыла соединение.
                    if (bytesRead == 0)
                    {
                        break;
                    }

                    string chunk = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    responseBuilder.Append(chunk);

                    Console.WriteLine($"[CLIENT] Получена порция: {chunk}");
                }

                Console.WriteLine("[CLIENT] Полный ответ сервера:");
                Console.WriteLine(responseBuilder.ToString());

                Console.WriteLine("[CLIENT] Соединение закрыто");
            }
            catch (SocketException ex)
            {
                Console.WriteLine($"[CLIENT] Сетевая ошибка: {ex.Message}");
            }
            catch (InvalidOperationException ex)
            {
                Console.WriteLine($"[CLIENT] Ошибка состояния клиента: {ex.Message}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[CLIENT] Непредвиденная ошибка: {ex.Message}");
            }
            finally
            {
                Console.WriteLine("[CLIENT] Клиент завершил работу");
            }
        }

        // Разбираем порт из аргументов командной строки.
        // Если аргумент отсутствует или некорректен, используется порт по умолчанию.
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
                $"[CLIENT] Некорректный порт \"{args[0]}\". Используется порт по умолчанию {defaultPort}");
            return defaultPort;
        }
    }
}
