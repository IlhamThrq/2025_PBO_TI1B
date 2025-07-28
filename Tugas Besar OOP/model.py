import datetime
from abc import ABC, abstractmethod

class BaseOrder(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

class OrderInventaris(BaseOrder):
    def __init__(
        self, 
        nama_pelanggan, 
        status_pelanggan, 
        list_barang, 
        jenis_transaksi,
        jumlah, 
        metode_pembayaran, 
        tanggal_order, 
        tanggal_kembali=None,
        total=0, id_order=None
    ):
        self.id_order = id_order
        self.nama_pelanggan = nama_pelanggan.strip() or "Tanpa Nama"
        self.status_pelanggan = status_pelanggan.strip()
        self.list_barang = list_barang  # list of str/barang
        self.jenis_transaksi = jenis_transaksi.strip()
        self.jumlah = jumlah
        self.metode_pembayaran = metode_pembayaran.strip()
        self.tanggal_order = self._parse_tanggal(tanggal_order)
        self.tanggal_kembali = self._parse_tanggal(tanggal_kembali) if tanggal_kembali else None
        self.total = int(total)

    def _parse_tanggal(self, tgl):
        if not tgl:
            return None
        if isinstance(tgl, datetime.date):
            return tgl
        try:
            return datetime.datetime.strptime(tgl, "%Y-%m-%d").date()
        except:
            return datetime.date.today()

    def to_dict(self):
        return {
            "id_order": self.id_order,
            "nama_pelanggan": self.nama_pelanggan,
            "status_pelanggan": self.status_pelanggan,
            "list_barang": ",".join(self.list_barang),
            "jenis_transaksi": self.jenis_transaksi,
            "jumlah": self.jumlah,
            "metode_pembayaran": self.metode_pembayaran,
            "tanggal_order": self.tanggal_order.strftime("%Y-%m-%d"),
            "tanggal_kembali": self.tanggal_kembali.strftime("%Y-%m-%d") if self.tanggal_kembali else "",
            "total": self.total
        }

    def __repr__(self):
        return (
            f"OrderInventaris({self.id_order}, {self.nama_pelanggan}, {self.status_pelanggan}, "
            f"{self.list_barang}, {self.jenis_transaksi}, {self.jumlah}, {self.metode_pembayaran}, "
            f"{self.tanggal_order}, {self.tanggal_kembali}, {self.total})"
        )
