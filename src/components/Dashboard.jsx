
import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import AgentInsights from './AgentInsights';
import { getDashboardData } from '../api';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getDashboardData()
            .then(res => {
                setData(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!data) {
        return <div>No data available.</div>;
    }

    const { location } = data;

    return (
        <div>
            <h1>{data.make} {data.model} ({data.year})</h1>
            <p>VIN: {data.vin}</p>
            <p>Odometer: {data.odometer.data.distance} {data.odometer.unit}</p>
            
            <h2>Vehicle Metrics</h2>
            <p>Tire Pressure: {JSON.stringify(data.tire_pressure)}</p>
            <p>Battery: {JSON.stringify(data.battery)}</p>
            <p>Engine Oil: {JSON.stringify(data.engine_oil)}</p>

            <h2>Location</h2>
            <MapContainer center={[location.data.latitude, location.data.longitude]} zoom={13} style={{ height: '400px' }}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={[location.data.latitude, location.data.longitude]}>
                    <Popup>
                        A pretty CSS3 popup. <br /> Easily customizable.
                    </Popup>
                </Marker>
            </MapContainer>

            <AgentInsights />
        </div>
    );
};

export default Dashboard;
