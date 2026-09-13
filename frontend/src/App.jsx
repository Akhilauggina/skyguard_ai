import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard";
import Stations from "./pages/Stations";
import Weather from "./pages/Weather";
import Predictions from "./pages/Predictions";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MainLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="stations" element={<Stations />} />
          <Route path="weather" element={<Weather />} />
          <Route path="predictions" element={<Predictions />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
