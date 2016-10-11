import os
import sys

from halimun import Halimun
import numpy as np

class TestHalimun:

    def test_simple_search_provinsi(self):
        hal = Halimun("172.19.0.11")
        id_admin = hal.cari_admin("jakarta", "provinsi")
        assert id_admin == 31

    def test_pilih_desa_dari_provinsi(self):
        geolevel = "provinsi"
        geoname = "jakarta"
        quantity = 8
        div_factor = np.int(1e8)
        hal = Halimun("172.19.0.11")
        hasil = hal.pilih_banyak_desa(geoname, geolevel, quantity)
        id_admin = hal.cari_admin(geoname, geolevel)
        assert hasil[0] == geolevel
        assert hasil[1] == geoname
        assert len(hasil[2]) == quantity
        for i in hasil[2]:
            assert i / div_factor == id_admin

    def test_pilih_desa_dari_kabupaten(self):
        geolevel = "kabupaten"
        geoname = "jakarta selatan"
        quantity = 6
        div_factor = np.int(1e6)
        hal = Halimun("172.19.0.11")
        hasil = hal.pilih_banyak_desa(geoname, geolevel, quantity)
        id_admin = hal.cari_admin(geoname, geolevel)
        assert hasil[0] == geolevel
        assert hasil[1] == geoname
        assert len(hasil[2]) == quantity
        for i in hasil[2]:
            assert i / div_factor == id_admin

    def test_pilih_desa_dari_kecamatan(self):
        geolevel = "kecamatan"
        geoname = "tebet"
        quantity = 5
        div_factor = np.int(1e3)
        hal = Halimun("172.19.0.11")
        hasil = hal.pilih_banyak_desa(geoname, geolevel, quantity)
        id_admin = hal.cari_admin(geoname, geolevel)
        assert hasil[0] == geolevel
        assert hasil[1] == geoname
        assert len(hasil[2]) == quantity
        for i in hasil[2]:
            assert i / div_factor == id_admin

    def test_pilih_desa_dari_kelurahan(self):
        geolevel = "kelurahan"
        geoname = "tebet timur"
        quantity = 3
        div_factor = np.int(1e0)
        hal = Halimun("172.19.0.11")
        hasil = hal.pilih_banyak_desa(geoname, geolevel, quantity)
        id_admin = hal.cari_admin(geoname, geolevel)
        assert hasil[0] == geolevel
        assert hasil[1] == geoname
        assert len(hasil[2]) == quantity
        for i in hasil[2]:
            assert i / div_factor == id_admin

    def test_pilih_desa_dari_cresta(self):
        geolevel = "cresta"
        geoname = "1"
        quantity = 5
        hal = Halimun("172.19.0.11")
        hasil = hal.pilih_banyak_desa(geoname, geolevel, quantity)
        assert hasil[0] == geolevel
        assert hasil[1] == geoname
        assert len(hasil[2]) == quantity

    def test_cari_provinsi_num_cresta(self):
        id_cresta = 2
        hal = Halimun("172.19.0.11")
        id_provinsi = hal.cari_provinsi_dari_cresta(id_cresta)
        assert isinstance(id_provinsi, int)

    def test_cari_provinsi_num_cresta_decimal(self):
        id_cresta = 2.2
        hal = Halimun("172.19.0.11")
        id_provinsi = hal.cari_provinsi_dari_cresta(id_cresta)
        assert isinstance(id_provinsi, int)

    def test_cari_provinsi_num_cresta_string(self):
        id_cresta = "2.2"
        hal = Halimun("172.19.0.11")
        id_provinsi = hal.cari_provinsi_dari_cresta(id_cresta)
        assert isinstance(id_provinsi, int)

    def test_cari_provinsi_num_cresta_string_romawi(self):
        id_cresta = "I"
        hal = Halimun("172.19.0.11")
        try:
            id_provinsi = hal.cari_provinsi_dari_cresta(id_cresta)
        except RuntimeError, e:
            assert True

    def test_cari_kecamatan_num_kodepos(self):
        id_kodepos = 12810
        hal = Halimun("172.19.0.11")
        id_kecamatan = hal.cari_kecamatan_dari_kodepos(id_kodepos)
        assert isinstance(id_kecamatan, int)

    def test_cari_kecamatan_num_kodepos_string(self):
        id_kodepos = "12810"
        hal = Halimun("172.19.0.11")
        id_kecamatan = hal.cari_kecamatan_dari_kodepos(id_kodepos)
        assert isinstance(id_kecamatan, int)

    def test_cari_kecamatan_num_string_non(self):
        id_kodepos = "12810A"
        hal = Halimun("172.19.0.11")
        id_kecamatan = hal.cari_kecamatan_dari_kodepos(id_kodepos)
        assert isinstance(id_kecamatan, int)

    def test_pilih_desa_dari_kodepos(self):
        geolevel = "kodepos"
        geoname = "12810A"
        quantity = 5
        hal = Halimun("172.19.0.11")
        hasil = hal.pilih_banyak_desa(geoname, geolevel, quantity)
        assert hasil[0] == geolevel
        assert hasil[1] == geoname
        assert len(hasil[2]) == quantity

