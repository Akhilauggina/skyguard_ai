import { useEffect, useState } from "react";
import {
  MdLocationOn,
  MdCloud,
  MdInsights,
  MdWarning,
} from "react-icons/md";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import API from "../api/axios";
import StatCard from "../components/StatCard";

export default function Dashboard() {
  const [stations, setStations] = useState([]);
  const [readings, setReadings] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [stRes, wrRes, prRes] = await Promise.allSettled([
          API.get("/stations"),
          API.get("/weather-readings"),
          API.get("/predictions"),
        ]);
        if (stRes.status === "fulfilled") setStations(stRes.value.data);
        if (wrRes.status === "fulfilled") setReadings(wrRes.value.data);
        if (prRes.status === "fulfilled") setPredictions(prRes.value.data);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const anomalyCount = predictions.filter((p) => p.is_anomaly).length;

  // Prepare chart data from latest readings
  const chartData = readings
    .slice(-20)
    .map((r) => ({
      time: new Date(r.recorded_at).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      temperature: r.temperature,
      humidity: r.humidity,
      pressure: r.pressure,
    }));

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin h-8 w-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          icon={MdLocationOn}
          title="Stations"
          value={stations.length}
          subtitle="Active monitoring stations"
          color="indigo"
        />
        <StatCard
          icon={MdCloud}
          title="Readings"
          value={readings.length}
          subtitle="Total weather readings"
          color="blue"
        />
        <StatCard
          icon={MdInsights}
          title="Predictions"
          value={predictions.length}
          subtitle="AI predictions made"
          color="green"
        />
        <StatCard
          icon={MdWarning}
          title="Anomalies"
          value={anomalyCount}
          subtitle="Detected anomalies"
          color="red"
        />
      </div>

      {/* Temperature chart */}
      {chartData.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Recent Temperature Readings
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="tempGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="time" fontSize={12} />
              <YAxis fontSize={12} />
              <Tooltip />
              <Area
                type="monotone"
                dataKey="temperature"
                stroke="#6366f1"
                fill="url(#tempGrad)"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

