import asyncio
import concurrent.futures
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import QueryProcessor
import time
import Logger

class CommMonitor:

    def __init__(self):
        print('I am going to do something with this one day')


class ComServer:

    ji = QueryProcessor.ReturnQuery()
    h_ip = None
    h_port = None
    server = None
    loop = None
    thread_pool = None
    active_connections = {}  #todo possibly going to be used for as a dictionary for connections

    async def close_connection(self, writer):
        """

        :param writer:
        """
        writer.close()
        await writer.wait_closed()

    async def interpret_request(self, data, writer):
        """
        Asynchronous and Multi-threaded - Analyze the data from the client and determine the function to perform then
        send response message - logic portion
        :param data:
        :param writer:
        """

        #runs the decision tree in a different thread so there is no blocking operation during
        message, close_connection = await self.loop.run_in_executor(self.thread_pool, self.decision_tree, data)
        try:
            await self.send_response(message, writer, close_connection)

        except KeyboardInterrupt:
            Logger.Log("Logger Manually Stopped", 3)

    async def send_response(self, outgoing_msg, writer, close_after_response):
        """
        Asynchronous(main event loop) - Encodes the response to client and sends it. Initiates connection closure if
        requested by the client - send comms portion
        :param outgoing_msg:
        :param writer:
        :param close_after_response:
        """
        writer.write(outgoing_msg.encode('utf-8'))
        await writer.drain()
        await self.close_connection(writer)

        if close_after_response:
            await self.close_connection(writer)

    async def communicate(self, reader, writer):
        """
        Asynchronous (main event loop) - Communicates with the connected client and decodes and sends data off to
        appropriate functions - read comms portion
        :param reader: stream reader
        :type reader:
        :param writer: stream writer
        """
        try:
            data = await reader.read(100000000)
            await self.interpret_request(data.decode('utf-8'), writer)

        except asyncio.exceptions.IncompleteReadError as error:
            Logger.Log(error.args, 1)

    async def main(self):
        """
        Asynchronous (main event loop) - Starts the server with given parameters and keeps it running accepting new
        connections - initiate server portion
        """
        self.server = await asyncio.start_server(self.communicate, self.h_ip, self.h_port)

        self.loop = asyncio.get_running_loop()

        async with self.server:
            await self.server.serve_forever()

    def server_init(self, h_ip, h_port):
        """
        None - Function to be called outside this class and initiates server startup
        :param h_ip: ip address
        :type h_ip: str
        :param h_port: port number
        :type h_port: int
        """
        self.ji = QueryProcessor.ReturnQuery()
        self.h_ip = h_ip
        self.h_port = h_port
        self.thread_pool = ThreadPoolExecutor(4)
        Logger.Log("**** App Started ****", 3)

        try:
            asyncio.run(self.main())

        except KeyboardInterrupt:
            Logger.Log("Logger Manually Stopped", 3)

        except Exception as e:
            Logger.Log(e.args, 1, "Main Loop")

    def decision_tree(self, data):
        """
        Code for specific application resides here
        :param data: incoming comms
        :type data: dict
        :rtype: tuple[dict, bool]
        """

