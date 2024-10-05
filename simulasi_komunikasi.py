import tkinter as tk
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DistributedSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulasi Model Komunikasi Sistem Terdistribusi")
        self.root.configure(bg="#282c34")

        # Mengatur layout menggunakan grid
        self.root.columnconfigure(0, weight=1)  

        # Label untuk simulasi model komunikasi
        self.label = tk.Label(self.root, text="Pilih Simulasi Model Komunikasi:", bg="#282c34", fg="white", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, pady=10, sticky="nsew")  

        # Frame untuk tombol
        button_frame = tk.Frame(self.root, bg="#282c34")
        button_frame.grid(row=1, column=0, pady=5, sticky="nsew")

        # Tombol untuk masing-masing simulasi model
        self.request_response_btn = tk.Button(button_frame, text="Request-Response", command=self.start_request_response_simulation, 
                                              bg="#61afef", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.request_response_btn.pack(side=tk.LEFT, padx=5)  

        self.pub_sub_btn = tk.Button(button_frame, text="Publish-Subscribe", command=self.start_publish_subscribe_simulation, 
                                     bg="#e06c75", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.pub_sub_btn.pack(side=tk.LEFT, padx=5)  

        self.rpc_btn = tk.Button(button_frame, text="RPC", command=self.start_rpc_simulation, 
                                 bg="#98c379", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.rpc_btn.pack(side=tk.LEFT, padx=5)  

        # Label untuk simulasi permasalahan
        self.problem_label = tk.Label(self.root, text="Pilih Simulasi Permasalahan:", bg="#282c34", fg="white", font=("Helvetica", 16))
        self.problem_label.grid(row=2, column=0, pady=10, sticky="nsew")  

        # Frame untuk tombol permasalahan
        problem_frame = tk.Frame(self.root, bg="#282c34")
        problem_frame.grid(row=3, column=0, pady=5, sticky="nsew")

        # Tombol untuk permasalahan Request-Response
        self.request_response_timeout_btn = tk.Button(problem_frame, text="Timeout RR", command=self.start_request_response_timeout_simulation, 
                                                      bg="#d19a66", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.request_response_timeout_btn.pack(side=tk.LEFT, padx=5)  

        self.request_response_error_btn = tk.Button(problem_frame, text="Error Koneksi RR", command=self.start_request_response_error_simulation, 
                                                      bg="#d19a66", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.request_response_error_btn.pack(side=tk.LEFT, padx=5)  

        self.request_response_process_error_btn = tk.Button(problem_frame, text="Error Proses RR", command=self.start_request_response_process_error_simulation, 
                                                             bg="#d19a66", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.request_response_process_error_btn.pack(side=tk.LEFT, padx=5)  

        # Tombol untuk permasalahan Publish-Subscribe
        self.pub_sub_receive_error_btn = tk.Button(problem_frame, text="Gagal Menerima", command=self.start_publish_subscribe_receive_error_simulation, 
                                                    bg="#e06c75", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.pub_sub_receive_error_btn.pack(side=tk.LEFT, padx=5)  

        self.pub_sub_publish_error_btn = tk.Button(problem_frame, text="Publish Gagal", command=self.start_publish_subscribe_publish_error_simulation, 
                                                    bg="#e06c75", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.pub_sub_publish_error_btn.pack(side=tk.LEFT, padx=5)  

        self.pub_sub_duplicate_message_btn = tk.Button(problem_frame, text="Pesan Duplikat", command=self.start_publish_subscribe_duplicate_message_simulation, 
                                                        bg="#e06c75", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.pub_sub_duplicate_message_btn.pack(side=tk.LEFT, padx=5)  

        # Tombol untuk permasalahan RPC
        self.rpc_timeout_btn = tk.Button(problem_frame, text="Timeout RPC", command=self.start_rpc_timeout_simulation, 
                                          bg="#98c379", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.rpc_timeout_btn.pack(side=tk.LEFT, padx=5)  

        self.rpc_execution_error_btn = tk.Button(problem_frame, text="Gagal Eksekusi RPC", command=self.start_rpc_execution_error_simulation, 
                                                  bg="#98c379", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.rpc_execution_error_btn.pack(side=tk.LEFT, padx=5)  

        self.rpc_connection_error_btn = tk.Button(problem_frame, text="Koneksi Gagal RPC", command=self.start_rpc_connection_error_simulation, 
                                                   bg="#98c379", fg="white", font=("Helvetica", 10, "bold"), width=15)
        self.rpc_connection_error_btn.pack(side=tk.LEFT, padx=5)  

        # Textbox untuk output log
        self.output_text = tk.Text(self.root, height=10, width=50, bg="#abb2bf", fg="black", font=("Courier", 12))
        self.output_text.grid(row=4, column=0, pady=10, sticky="nsew")  

        # Setup matplotlib figure dan canvas untuk grafis
        self.fig, (self.ax_data_flow, self.ax_throughput) = plt.subplots(2, figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=5, column=0, pady=10, sticky="nsew")  
        self.data_flow = []
        self.throughput_data = []
        self.start_time = time.time()

        self.node_colors = {
            "Client": "blue",
            "Server": "green",
            "Publisher": "orange",
            "Subscriber 1": "purple",
            "Subscriber 2": "red",
            "RPC Server": "cyan"
        }

        # Animasi untuk throughput
        self.ani = FuncAnimation(self.fig, self.animate, interval=1000)

    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def update_graph(self, nodes, connections):
        self.ax_data_flow.clear()
        self.ax_data_flow.set_title("Aliran Data", fontsize=14)
        self.ax_data_flow.set_facecolor('#1e2127')
        for node, pos in nodes.items():
            self.ax_data_flow.scatter(*pos, label=node, color=self.node_colors.get(node, "black"), s=200, edgecolors="white", linewidths=2)
        for start, end in connections:
            start_pos = nodes[start]
            end_pos = nodes[end]
            self.ax_data_flow.annotate("", xy=end_pos, xytext=start_pos,
                                       arrowprops=dict(facecolor='yellow', edgecolor='yellow', linewidth=2, arrowstyle="->", linestyle="dashed"))
        self.ax_data_flow.legend(facecolor='#abb2bf', edgecolor='white')
        self.canvas.draw()

    def animate(self, i):
        self.ax_throughput.clear()
        self.ax_throughput.set_title("Throughput (Pesan per detik)", fontsize=14)
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            throughput = len(self.data_flow) / elapsed_time
            self.throughput_data.append(throughput)
        else:
            self.throughput_data.append(0)
        self.ax_throughput.plot(self.throughput_data, color='cyan', label='Throughput')
        self.ax_throughput.set_facecolor('#1e2127')
        self.ax_throughput.legend(facecolor='#abb2bf', edgecolor='white')
        self.canvas.draw()

    ### Simulasi untuk Request-Response ###
    
    def start_request_response_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.request_response_simulation).start()

    def start_request_response_timeout_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.request_response_timeout).start()

    def start_request_response_error_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.request_response_connection_error).start()

    def start_request_response_process_error_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.request_response_process_error).start()

    def request_response_simulation(self):
        nodes = {"Client": (0.2, 0.5), "Server": (0.8, 0.5)}
        self.update_graph(nodes, [])
        self.log("Model: Request-Response\nClient meminta data, Server merespons.")
        for i in range(5):
            client_message = f"Client meminta data ke Server (Request {i + 1})"
            self.log(client_message)
            self.update_graph(nodes, [("Client", "Server")])
            time.sleep(1)
            server_message = f"Server merespons dengan data (Response {i + 1})"
            self.log(server_message)
            self.data_flow.append(("Client", "Server"))
            self.update_graph(nodes, [("Server", "Client")])
            time.sleep(1)

    def request_response_timeout(self):
        nodes = {"Client": (0.2, 0.5), "Server": (0.8, 0.5)}
        self.update_graph(nodes, [])
        self.log("Model: Request-Response (Timeout)")
        for i in range(5):
            client_message = f"Client meminta data ke Server (Request {i + 1})"
            self.log(client_message)
            self.update_graph(nodes, [("Client", "Server")])
            time.sleep(2)  # Simulate timeout by waiting longer
            self.log("Server tidak merespons dalam waktu yang ditentukan (Timeout)")
            self.data_flow.append(("Client", "Server"))
            self.update_graph(nodes, [])

    def request_response_connection_error(self):
        nodes = {"Client": (0.2, 0.5), "Server": (0.8, 0.5)}
        self.update_graph(nodes, [])
        self.log("Model: Request-Response (Error Koneksi)")
        for i in range(5):
            client_message = f"Client mencoba terhubung ke Server (Request {i + 1})"
            self.log(client_message)
            self.update_graph(nodes, [("Client", "Server")])
            time.sleep(1)
            self.log("Koneksi ke Server gagal")
            self.data_flow.append(("Client", "Server"))
            self.update_graph(nodes, [])

    def request_response_process_error(self):
        nodes = {"Client": (0.2, 0.5), "Server": (0.8, 0.5)}
        self.update_graph(nodes, [])
        self.log("Model: Request-Response (Error Proses)")
        for i in range(5):
            client_message = f"Client meminta data ke Server (Request {i + 1})"
            self.log(client_message)
            self.update_graph(nodes, [("Client", "Server")])
            time.sleep(1)
            self.log("Server mengalami kesalahan saat memproses permintaan")
            self.data_flow.append(("Client", "Server"))
            self.update_graph(nodes, [("Server", "Client")])
            time.sleep(1)

    ### Simulasi untuk Publish-Subscribe ###
    
    def start_publish_subscribe_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.publish_subscribe_simulation).start()

    def start_publish_subscribe_receive_error_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.publish_subscribe_receive_error).start()

    def start_publish_subscribe_publish_error_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.publish_subscribe_publish_error).start()

    def start_publish_subscribe_duplicate_message_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.publish_subscribe_duplicate_message).start()

    def publish_subscribe_simulation(self):
        nodes = {"Publisher": (0.5, 0.5), "Subscriber 1": (0.2, 0.8), "Subscriber 2": (0.8, 0.2)}
        self.update_graph(nodes, [])
        self.log("Model: Publish-Subscribe")
        for i in range(5):
            message = f"Pesan {i + 1}"
            self.log(f"Publisher mengirim: {message}")
            self.update_graph(nodes, [("Publisher", "Subscriber 1"), ("Publisher", "Subscriber 2")])
            self.data_flow.append(("Publisher", "Subscriber 1"))
            self.data_flow.append(("Publisher", "Subscriber 2"))
            time.sleep(1)

    def publish_subscribe_receive_error(self):
        nodes = {"Publisher": (0.5, 0.5), "Subscriber 1": (0.2, 0.8), "Subscriber 2": (0.8, 0.2)}
        self.update_graph(nodes, [])
        self.log("Model: Publish-Subscribe (Gagal Menerima Pesan)")
        for i in range(5):
            message = f"Pesan {i + 1}"
            self.log(f"Publisher mengirim: {message}")
            self.update_graph(nodes, [("Publisher", "Subscriber 1"), ("Publisher", "Subscriber 2")])
            time.sleep(1)
            if i == 2:  # Simulate receiving error on the third message
                self.log("Subscriber 1 gagal menerima pesan")
                continue
            self.data_flow.append(("Publisher", "Subscriber 1"))
            self.data_flow.append(("Publisher", "Subscriber 2"))
            self.update_graph(nodes, [("Subscriber 1", "Subscriber 2")])
            time.sleep(1)

    def publish_subscribe_publish_error(self):
        nodes = {"Publisher": (0.5, 0.5), "Subscriber 1": (0.2, 0.8), "Subscriber 2": (0.8, 0.2)}
        self.update_graph(nodes, [])
        self.log("Model: Publish-Subscribe (Publish Gagal)")
        for i in range(5):
            message = f"Pesan {i + 1}"
            if i == 2:  # Simulate publish error on the third message
                self.log("Publisher gagal mengirim pesan")
                self.update_graph(nodes, [])
                continue
            self.log(f"Publisher mengirim: {message}")
            self.update_graph(nodes, [("Publisher", "Subscriber 1"), ("Publisher", "Subscriber 2")])
            self.data_flow.append(("Publisher", "Subscriber 1"))
            self.data_flow.append(("Publisher", "Subscriber 2"))
            time.sleep(1)

    def publish_subscribe_duplicate_message(self):
        nodes = {"Publisher": (0.5, 0.5), "Subscriber 1": (0.2, 0.8), "Subscriber 2": (0.8, 0.2)}
        self.update_graph(nodes, [])
        self.log("Model: Publish-Subscribe (Pesan Duplikat)")
        for i in range(5):
            message = f"Pesan {i + 1}"
            self.log(f"Publisher mengirim: {message}")
            self.update_graph(nodes, [("Publisher", "Subscriber 1"), ("Publisher", "Subscriber 2")])
            self.data_flow.append(("Publisher", "Subscriber 1"))
            self.data_flow.append(("Publisher", "Subscriber 2"))
            time.sleep(1)
            if i == 2:  # Simulate duplicate message on the third message
                self.log("Subscriber 1 menerima pesan duplikat")
                continue

    ### Simulasi untuk RPC ###
    
    def start_rpc_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.rpc_simulation).start()

    def start_rpc_timeout_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.rpc_timeout).start()

    def start_rpc_execution_error_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.rpc_execution_error).start()

    def start_rpc_connection_error_simulation(self):
        self.reset_simulation()
        threading.Thread(target=self.rpc_connection_error).start()

    def rpc_simulation(self):
        nodes = {"Client": (0.2, 0.5), "RPC Server": (0.8, 0.5)}
        self.update_graph(nodes, [])
        self.log("Model: RPC")
        for i in range(5):
            client_message = f"Client meminta prosedur (Request {i + 1})"
            self.log(client_message)
            self.update_graph(nodes, [("Client", "RPC Server")])
            time.sleep(1)
            server_message = f"RPC Server merespons (Response {i + 1})"
            self.log(server_message)
            self.data_flow.append(("Client", "RPC Server"))
            self.update_graph(nodes, [("RPC Server", "Client")])
            time.sleep(1)

    def rpc_timeout(self):
        nodes = {"Client": (0.2, 0.5), "RPC Server": (0.8, 0.5)}
        self.update_graph(nodes, [])
        self.log("Model: RPC (Timeout)")
        for i in range(5):
            client_message = f"Client meminta prosedur (Request {i + 1})"
            self.log(client_message)
            self.update_graph(nodes, [("Client", "RPC Server")])
            time.sleep(2)  # Simulate timeout by waiting longer
            self.log("RPC Server tidak merespons dalam waktu yang ditentukan (Timeout)")
            self.data_flow.append(("Client", "RPC Server"))
            self.update_graph(nodes, [])

    def rpc_execution_error(self):
        nodes = {"Client": (0.2, 0.5), "RPC Server": (0.8, 0.5)}
        self.update_graph(nodes, [])
        self.log("Model: RPC (Gagal Eksekusi)")
        for i in range(5):
            client_message = f"Client meminta prosedur (Request {i + 1})"
            self.log(client_message)
            self.update_graph(nodes, [("Client", "RPC Server")])
            time.sleep(1)
            self.log("RPC Server gagal mengeksekusi prosedur yang diminta")
            self.data_flow.append(("Client", "RPC Server"))
            self.update_graph(nodes, [])

    def rpc_connection_error(self):
        nodes = {"Client": (0.2, 0.5), "RPC Server": (0.8, 0.5)}
        self.update_graph(nodes, [])
        self.log("Model: RPC (Koneksi Gagal)")
        for i in range(5):
            client_message = f"Client mencoba terhubung ke RPC Server (Request {i + 1})"
            self.log(client_message)
            self.update_graph(nodes, [("Client", "RPC Server")])
            time.sleep(1)
            self.log("Koneksi ke RPC Server gagal")
            self.data_flow.append(("Client", "RPC Server"))
            self.update_graph(nodes, [])

    def reset_simulation(self):
        self.data_flow.clear()
        self.throughput_data.clear()
        self.start_time = time.time()
        self.ax_data_flow.clear()
        self.ax_throughput.clear()
        self.canvas.draw()
        self.output_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DistributedSystem(root)
    root.mainloop()