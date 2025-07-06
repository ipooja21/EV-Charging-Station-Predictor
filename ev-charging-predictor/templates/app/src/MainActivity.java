package com.example.navicintegration;

import android.location.GnssStatus;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private LocationManager locationManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
        registerNavICStatus();
    }

    private void registerNavICStatus() {
        locationManager.registerGnssStatusCallback(new GnssStatus.Callback() {
            @Override
            public void onSatelliteStatusChanged(GnssStatus status) {
                int satelliteCount = status.getSatelliteCount();
                for (int i = 0; i < satelliteCount; i++) {
                    int svid = status.getSvid(i);
                    String constellation = getConstellationName(status.getConstellationType(i));
                    if (constellation.equals("NavIC")) {
                        Log.d("NavIC", "NavIC Satellite detected: SVID " + svid);
                    }
                }
            }
        });
    }

    private String getConstellationName(int type) {
        switch (type) {
            case GnssStatus.CONSTELLATION_GPS: return "GPS";
            case GnssStatus.CONSTELLATION_GLONASS: return "GLONASS";
            case GnssStatus.CONSTELLATION_GALILEO: return "Galileo";
            case GnssStatus.CONSTELLATION_BEIDOU: return "BeiDou";
            case GnssStatus.CONSTELLATION_QZSS: return "QZSS";
            case GnssStatus.CONSTELLATION_IRNSS: return "NavIC";
            default: return "Unknown";
        }
    }
}
