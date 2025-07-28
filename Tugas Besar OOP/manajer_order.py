from model import OrderInventaris
import database
import pandas as pd

class ManajerOrderInventaris:
    def __init__(self):
        self.refresh_data()

    def refresh_data(self):
        rows = database.fetch_query("SELECT * FROM order_inventaris ORDER BY tanggal_order DESC")
        self._all_order = [self._row_to_obj(row) for row in rows] if rows else []

    def _row_to_obj(self, row):
        return OrderInventaris(
            id_order=row["id_order"],
            nama_pelanggan=row["nama_pelanggan"],
            status_pelanggan=row["status_pelanggan"],
            list_barang=row["list_barang"].split(","),
            jenis_transaksi=row["jenis_transaksi"],
            jumlah=row["jumlah"],
            metode_pembayaran=row["metode_pembayaran"],
            tanggal_order=row["tanggal_order"],
            tanggal_kembali=row["tanggal_kembali"],
            total=row["total"]
        )

    def tambah_order(self, order: OrderInventaris) -> bool:
        res = database.execute_query(
            """INSERT INTO order_inventaris 
            (nama_pelanggan, status_pelanggan, list_barang, jenis_transaksi, jumlah, metode_pembayaran, tanggal_order, tanggal_kembali, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                order.nama_pelanggan, order.status_pelanggan, ",".join(order.list_barang), 
                order.jenis_transaksi, order.jumlah, order.metode_pembayaran, 
                order.tanggal_order.strftime("%Y-%m-%d"), 
                order.tanggal_kembali.strftime("%Y-%m-%d") if order.tanggal_kembali else "",
                order.total
            )
        )
        if res:
            self.refresh_data()
            return True
        return False

    def hapus_order(self, id_order):
        res = database.execute_query("DELETE FROM order_inventaris WHERE id_order = ?", (id_order,))
        if res:
            self.refresh_data()
            return True
        return False

    def get_all_orders(self):
        return self._all_order

    def get_dataframe_order(self):
        return pd.DataFrame([o.to_dict() for o in self._all_order])

    def total_pendapatan(self):
        return sum([o.total for o in self._all_order if o.jenis_transaksi != "Peminjaman"])
