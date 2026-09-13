import { useEffect, useState } from "react";
import { MdAdd, MdDelete } from "react-icons/md";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import API from "../api/axios";

export default function Weather() {
  const [readings, setReadings] = useState([]);
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    station_id: "",
    temperature: "",
    pressure: "",
    humidity: "",
    recorded_at: "",
  });

  const fetchData = async () => {
    try {
      const [rRes, sRes] = await Promise.allSettled([
        API.get("/weather-readings"),
        API.get("/stations"),
      ]);
      if (rRes.status === "fulfilled") setReadings(rRes.value.data);
      if (sRes.status === "fulfilled") setStations(sRes.value.data);
    } catch (err) {
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post("/weather-readings", {
        station_id: parseInt(form.station_id),
        temperature: parseFloat(form.temperature),
        pressure: parseFloat(form.pressure),
        humidity: parseFloat(form.humidity),
        recorded_at: new Date(form.recorded_at).toISOString(),
      });
      setShowForm(false);
      setForm({ station_id: "", temperature: "", pressure: "", humidity: "", recorded_at: "" });
      fetchData();
    } catch (err) {
      console.error("Error creating reading:", err);
      alert(err.response?.data?.detail || "Failed to create reading");
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this reading?")) return;
    try {
      await API.delete(`/weather-readings/${id}`);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to delete");
    }
  };

  // Chart data from latest 30 readings
  const chartData = readings.slice(-30).map((r) => ({
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
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Weather Readings</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition"
        >
          <MdAdd className="text-lg" />
          Add Reading
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="bg-white rounded-xl border border-gray-200 p-5 mb-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
        >
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Station
            </label>
            <select
              value={form.station_id}
              onChange={(e) => setForm({ ...form, station_id: e.target.value })}
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            >
              <option value="">Select station...</option>
              {stations.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.station_code})
                </option>
              ))}
            </select>
          </div>
          {[
            ["temperature", "Temperature (°C)"],
            ["pressure", "Pressure (hPa)"],
            ["humidity", "Humidity (%)"],
          ].map(([key, label]) => (
            <div key={key}>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {label}
              </label>
              <input
                type="number"
                step="any"
                value={form[key]}
                onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                required
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              />
            </div>
          ))}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Recorded At
            </label>
            <input
              type="datetime-local"
              value={form.recorded_at}
              onChange={(e) => setForm({ ...form, recorded_at: e.target.value })}
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div className="sm:col-span-2 lg:col-span-3 flex gap-2 justify-end">
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
            >
              Create
            </button>
          </div>
        </form>
      )}

      {/* Chart */}
      {chartData.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-5 mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Sensor Trends
          </h2>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="time" fontSize={12} />
              <YAxis fontSize={12} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="temperature" stroke="#6366f1" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="humidity" stroke="#10b981" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
              <tr>
                <th className="px-4 py-3">ID</th>
                <th className="px-4 py-3">Station</th>
                <th className="px-4 py-3">Temperature</th>
                <th className="px-4 py-3">Pressure</th>
                <th className="px-4 py-3">Humidity</th>
                <th className="px-4 py-3">Recorded At</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {readings.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-gray-400">
                    No weather readings found.
                  </td>
                </tr>
              ) : (
                readings.map((r) => (
                  <tr key={r.id} className="hover:bg-gray-50 transition">
                    <td className="px-4 py-3 font-mono text-xs">{r.id}</td>
                    <td className="px-4 py-3">{r.station_id}</td>
                    <td className="px-4 py-3">{r.temperature}°C</td>
                    <td className="px-4 py-3">{r.pressure} hPa</td>
                    <td className="px-4 py-3">{r.humidity}%</td>
                    <td className="px-4 py-3 text-xs">
                      {new Date(r.recorded_at).toLocaleString()}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => handleDelete(r.id)}
                        className="p-1.5 text-gray-400 hover:text-red-600 transition"
                      >
                        <MdDelete />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

