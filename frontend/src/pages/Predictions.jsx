import { useEffect, useState } from "react";
import { MdInsights } from "react-icons/md";
import API from "../api/axios";

export default function Predictions() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  // Manual predict form state
  const [showPredict, setShowPredict] = useState(false);
  const [predictForm, setPredictForm] = useState({
    temperature: "",
    humidity: "",
    pressure: "",
    wind_speed: "0",
    wind_direction: "0",
    visibility: "10",
    month: String(new Date().getMonth() + 1),
    hour: String(new Date().getHours()),
  });
  const [predictResult, setPredictResult] = useState(null);
  const [predicting, setPredicting] = useState(false);

  const fetchPredictions = async () => {
    try {
      const res = await API.get("/predictions");
      setPredictions(res.data);
    } catch (err) {
      console.error("Error fetching predictions:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPredictions();
  }, []);

  const handlePredict = async (e) => {
    e.preventDefault();
    setPredicting(true);
    setPredictResult(null);
    try {
      const res = await API.post("/predictions/predict", {
        temperature: parseFloat(predictForm.temperature),
        humidity: parseFloat(predictForm.humidity),
        pressure: parseFloat(predictForm.pressure),
        wind_speed: parseFloat(predictForm.wind_speed),
        wind_direction: parseFloat(predictForm.wind_direction),
        visibility: parseFloat(predictForm.visibility),
        month: parseInt(predictForm.month),
        hour: parseInt(predictForm.hour),
      });
      setPredictResult(res.data);
    } catch (err) {
      console.error("Prediction failed:", err);
      alert(err.response?.data?.detail || "Prediction failed");
    } finally {
      setPredicting(false);
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
        <h1 className="text-2xl font-bold text-gray-900">Predictions</h1>
        <button
          onClick={() => {
            setShowPredict(!showPredict);
            setPredictResult(null);
          }}
          className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition"
        >
          <MdInsights className="text-lg" />
          Manual Predict
        </button>
      </div>

      {/* Manual Predict Form */}
      {showPredict && (
        <div className="bg-white rounded-xl border border-gray-200 p-5 mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Run ML Prediction
          </h2>
          <form
            onSubmit={handlePredict}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
          >
            {[
              ["temperature", "Temperature (°C)"],
              ["humidity", "Humidity (%)"],
              ["pressure", "Pressure (hPa)"],
              ["wind_speed", "Wind Speed (m/s)"],
              ["wind_direction", "Wind Direction (°)"],
              ["visibility", "Visibility (km)"],
              ["month", "Month (1–12)"],
              ["hour", "Hour (0–23)"],
            ].map(([key, label]) => (
              <div key={key}>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {label}
                </label>
                <input
                  type="number"
                  step="any"
                  value={predictForm[key]}
                  onChange={(e) =>
                    setPredictForm({ ...predictForm, [key]: e.target.value })
                  }
                  required
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                />
              </div>
            ))}
            <div className="sm:col-span-2 lg:col-span-4 flex gap-2 justify-end">
              <button
                type="button"
                onClick={() => {
                  setShowPredict(false);
                  setPredictResult(null);
                }}
                className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={predicting}
                className="px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
              >
                {predicting ? "Predicting..." : "Predict"}
              </button>
            </div>
          </form>

          {/* Result */}
          {predictResult && (
            <div
              className={`mt-4 p-4 rounded-lg border ${
                predictResult.prediction === "Anomaly"
                  ? "bg-red-50 border-red-200"
                  : "bg-green-50 border-green-200"
              }`}
            >
              <div className="flex items-center gap-3">
                <span
                  className={`text-3xl font-bold ${
                    predictResult.prediction === "Anomaly"
                      ? "text-red-600"
                      : "text-green-600"
                  }`}
                >
                  {predictResult.prediction}
                </span>
                <span className="text-sm text-gray-500">
                  Anomaly Score: <strong>{predictResult.score}</strong>
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Predictions Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
              <tr>
                <th className="px-4 py-3">ID</th>
                <th className="px-4 py-3">Reading ID</th>
                <th className="px-4 py-3">Anomaly</th>
                <th className="px-4 py-3">Confidence</th>
                <th className="px-4 py-3">Severity</th>
                <th className="px-4 py-3">Model</th>
                <th className="px-4 py-3">Created At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {predictions.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-gray-400">
                    No predictions found. Use "Manual Predict" to test the ML
                    model.
                  </td>
                </tr>
              ) : (
                predictions.map((p) => (
                  <tr key={p.id} className="hover:bg-gray-50 transition">
                    <td className="px-4 py-3 font-mono text-xs">{p.id}</td>
                    <td className="px-4 py-3">{p.reading_id}</td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${
                          p.is_anomaly
                            ? "bg-red-100 text-red-700"
                            : "bg-green-100 text-green-700"
                        }`}
                      >
                        {p.is_anomaly ? "Yes" : "No"}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      {(p.confidence_score * 100).toFixed(1)}%
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${
                          p.severity === "HIGH"
                            ? "bg-red-100 text-red-700"
                            : p.severity === "MEDIUM"
                            ? "bg-amber-100 text-amber-700"
                            : "bg-gray-100 text-gray-600"
                        }`}
                      >
                        {p.severity}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-xs">
                      {p.model_name} v{p.model_version}
                    </td>
                    <td className="px-4 py-3 text-xs">
                      {new Date(p.created_at).toLocaleString()}
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

