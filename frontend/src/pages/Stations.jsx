import { useEffect, useState } from "react";
import { MdAdd, MdEdit, MdDelete } from "react-icons/md";
import API from "../api/axios";

export default function Stations() {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({
    station_code: "",
    name: "",
    city: "",
    state: "",
    latitude: "",
    longitude: "",
    status: "ACTIVE",
    installation_date: "",
  });

  const fetchStations = async () => {
    try {
      const res = await API.get("/stations");
      setStations(res.data);
    } catch (err) {
      console.error("Error fetching stations:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStations();
  }, []);

  const resetForm = () => {
    setForm({
      station_code: "",
      name: "",
      city: "",
      state: "",
      latitude: "",
      longitude: "",
      status: "ACTIVE",
      installation_date: "",
    });
    setEditingId(null);
    setShowForm(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      ...form,
      latitude: parseFloat(form.latitude),
      longitude: parseFloat(form.longitude),
    };
    try {
      if (editingId) {
        await API.put(`/stations/${editingId}`, payload);
      } else {
        await API.post("/stations", payload);
      }
      resetForm();
      fetchStations();
    } catch (err) {
      console.error("Error saving station:", err);
      alert(err.response?.data?.detail || "Failed to save station");
    }
  };

  const handleEdit = (station) => {
    setForm({
      station_code: station.station_code,
      name: station.name,
      city: station.city,
      state: station.state,
      latitude: String(station.latitude),
      longitude: String(station.longitude),
      status: station.status,
      installation_date: station.installation_date,
    });
    setEditingId(station.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!confirm("Are you sure you want to delete this station?")) return;
    try {
      await API.delete(`/stations/${id}`);
      fetchStations();
    } catch (err) {
      console.error("Error deleting station:", err);
      alert(err.response?.data?.detail || "Failed to delete station");
    }
  };

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
        <h1 className="text-2xl font-bold text-gray-900">Stations</h1>
        <button
          onClick={() => {
            resetForm();
            setShowForm(true);
          }}
          className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition"
        >
          <MdAdd className="text-lg" />
          Add Station
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="bg-white rounded-xl border border-gray-200 p-5 mb-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
        >
          {[
            ["station_code", "Station Code"],
            ["name", "Name"],
            ["city", "City"],
            ["state", "State"],
            ["latitude", "Latitude"],
            ["longitude", "Longitude"],
          ].map(([key, label]) => (
            <div key={key}>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {label}
              </label>
              <input
                type="text"
                value={form[key]}
                onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                required
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              />
            </div>
          ))}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={form.status}
              onChange={(e) => setForm({ ...form, status: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            >
              <option value="ACTIVE">Active</option>
              <option value="INACTIVE">Inactive</option>
              <option value="MAINTENANCE">Maintenance</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Installation Date
            </label>
            <input
              type="date"
              value={form.installation_date}
              onChange={(e) =>
                setForm({ ...form, installation_date: e.target.value })
              }
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div className="sm:col-span-2 lg:col-span-3 flex gap-2 justify-end">
            <button
              type="button"
              onClick={resetForm}
              className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
            >
              {editingId ? "Update" : "Create"}
            </button>
          </div>
        </form>
      )}

      {/* Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
              <tr>
                <th className="px-4 py-3">Code</th>
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">City</th>
                <th className="px-4 py-3">State</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Installed</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {stations.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-gray-400">
                    No stations found. Click "Add Station" to create one.
                  </td>
                </tr>
              ) : (
                stations.map((s) => (
                  <tr key={s.id} className="hover:bg-gray-50 transition">
                    <td className="px-4 py-3 font-mono text-xs">{s.station_code}</td>
                    <td className="px-4 py-3 font-medium text-gray-900">{s.name}</td>
                    <td className="px-4 py-3">{s.city}</td>
                    <td className="px-4 py-3">{s.state}</td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${
                          s.status === "ACTIVE"
                            ? "bg-green-100 text-green-700"
                            : s.status === "MAINTENANCE"
                            ? "bg-amber-100 text-amber-700"
                            : "bg-gray-100 text-gray-600"
                        }`}
                      >
                        {s.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">{s.installation_date}</td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => handleEdit(s)}
                        className="p-1.5 text-gray-400 hover:text-indigo-600 transition"
                      >
                        <MdEdit />
                      </button>
                      <button
                        onClick={() => handleDelete(s.id)}
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

