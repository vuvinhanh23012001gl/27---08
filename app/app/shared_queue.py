import queue

SIZE_QUEUE_RX_WEB_API = 50
SIZE_QUEUE_TX_WEB_LOG = 50
SIZE_QUEUE_TX_WEB_MAIN = 50
SIZE_QUEUE_RX_WEB_MAIN = 50
SIZE_QUEUE_ACCEPT_TAKE_PHOTO =  50
SIZE_QUEUE_CAPTURE_DETECT =  50
SIZE_QUEUE_SEND_DATA_DETECT = 10

queue_ = queue.Queue(maxsize = SIZE_QUEUE_ACCEPT_TAKE_PHOTO)
queue_accept_capture = queue.Queue(maxsize = SIZE_QUEUE_ACCEPT_TAKE_PHOTO)
queue_rx_web_api = queue.Queue(maxsize=SIZE_QUEUE_RX_WEB_API)
queue_tx_web_log = queue.Queue(maxsize=SIZE_QUEUE_TX_WEB_LOG)
queue_tx_web_main = queue.Queue(maxsize=SIZE_QUEUE_TX_WEB_MAIN)
queue_rx_web_main = queue.Queue(maxsize=SIZE_QUEUE_RX_WEB_MAIN)
process_capture_detect = queue.Queue(maxsize = SIZE_QUEUE_CAPTURE_DETECT)
queue_data_detect_send_client =  queue.Queue(maxsize = SIZE_QUEUE_SEND_DATA_DETECT)