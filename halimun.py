from difflib import get_close_matches
import os
import sys

import numpy as np
import redis

class Halimun:
    """
    Mencari administrasi geolevel in Indonesia
    """
    def __init__(self, server):
        self.rc = redis.StrictRedis(host=server, port=6379, db=0)
        # make sure all data exists in mercached
        self.daftar_provinsi = self.rc.hkeys("daftar-provinsi")
        self.daftar_kabupaten = self.rc.hkeys("daftar-kabupaten")
        self.daftar_kecamatan = self.rc.hkeys("daftar-kecamatan")
        self.daftar_kelurahan = self.rc.hkeys("daftar-kelurahan")
        self.daftar_geolevel = {
                "provinsi": self.daftar_provinsi,
                "kabupaten": self.daftar_kabupaten,
                "kecamatan": self.daftar_kecamatan,
                "kelurahan": self.daftar_kelurahan,
                }
        self.daftar_id_kelurahan = self.rc.get("daftar-id-kelurahan")
        self.daftar_id_kelurahan_num = np.array(
                self.daftar_id_kelurahan.split(","), dtype=np.int64)

    def cari_admin(self, query, geolevel):
        """
        query: admin yang hendak kau cari
        geolevel: level admin, salah satu dari (lowercase)
            - provinsi
            - kabupaten
            - kecamatan
            - kelurahan
        """
        query_norm = query.lower()
        key_geolevel = "daftar-%s" %(geolevel.lower())
        id_admin = self.rc.hget(key_geolevel, query_norm)
        if id_admin:
            return int(id_admin)
        else:
            try:
                key_approx = get_close_matches(
                        query_norm,
                        self.daftar_geolevel[geolevel.lower()])[0]
                id_admin = self.rc.hget(key_geolevel, key_approx)
                return int(id_admin)
            except IndexError:
                raise RuntimeError("Info admin %s %s not found" %(geolevel, query))

    def pilih_banyak_provinsi_dari_cresta(self, cresta):
        # TODO: mapping cresta to province
        # TODO: mapping province to cresta
        raise NotImplementedError

    def pilih_banyak_kecamatan_dari_kodepos(self, kodepos):
        raise NotImplementedError

    def pilih_banyak_desa(self, geoname, geolevel, quantity):
        """
        pilih desa
        """
        # 10 pangkat (jumlah digit relatif terhadap jumlah id digit kelurahan)
        geolevel_divisor = {
                "provinsi": np.int(1e8),
                "kabupaten": np.int(1e6),
                "kecamatan": np.int(1e3),
                "kelurahan": np.int(1e0),
                }

        # validasi tipe geolevel
        if geolevel in ("cresta", "provinsi", "kabupaten", "kodepos",
                "kecamatan", "kelurahan"):
            pass
        else:
            raise RuntimeError("Level administrasi tidak dikenali")

        if geolevel == "cresta":
            div_factor = geolevel_divisor["provinsi"]
            pilihan_provinsi = self.pilih_banyak_provinsi_dari_cresta(geoname)
            daftar_id_admin = pilihan_provinsi[0]
            dist_quantity = pilihan_provinsi[1]
        elif geolevel == "kodepos":
            div_factor = geolevel_divisor["kecamatan"]
            pilihan_kecamatan = self.pilih_banyak_kecamatan_dari_kodepos(geoname)
            daftar_id_admin = pilihan_kecamatan[0]
            dist_quantity = pilihan_kecamatan[1]
        else:
            id_admin = self.cari_admin(geoname, geolevel)
            div_factor = geolevel_divisor[geolevel]
            daftar_id_admin = np.array([id_admin], dtype=np.int)
            dist_quantity = np.array([quantity], dtype=np.int)

        div_id_kelurahan = self.daftar_id_kelurahan_num / div_factor

        temp_hasil = []
        for i,j in zip(daftar_id_admin, dist_quantity):
            ind_id_kelurahan = np.nonzero(div_id_kelurahan==i)[0]
            fil_id_kelurahan = self.daftar_id_kelurahan_num[ind_id_kelurahan]
            sam_id_kelurahan = np.random.choice(fil_id_kelurahan, size=j)
            temp_hasil.append(sam_id_kelurahan)
        final_hasil = np.hstack(np.array(temp_hasil))
        return (geolevel, geoname, final_hasil)

    def hitung_random_point(self, desa):
        """
        geometry_desa: dapet dari redis, bentuk string wkt
        """
        #geometry_desa = 
        pass

