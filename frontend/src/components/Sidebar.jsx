import { NavLink } from "react-router-dom";
import {
  MdDashboard,
  MdLocationOn,
  MdCloud,
  MdInsights,
} from "react-icons/md";

const links = [
  { to: "/", icon: MdDashboard, label: "Dashboard" },
  { to: "/stations", icon: MdLocationOn, label: "Stations" },
  { to: "/weather", icon: MdCloud, label: "Weather" },
  { to: "/predictions", icon: MdInsights, label: "Predictions" },
];

export default function Sidebar() {
  return (
    <aside className="w-60 bg-white border-r border-gray-200 h-[calc(100vh-4rem)] sticky top-16 flex flex-col py-4 shrink-0">
      <nav className="flex flex-col gap-1 px-3">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                isActive
                  ? "bg-indigo-50 text-indigo-700"
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              }`
            }
          >
            <Icon className="text-lg" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

