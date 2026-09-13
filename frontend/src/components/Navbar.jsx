import { WiDaySunny } from "react-icons/wi";
import { FiBell } from "react-icons/fi";

export default function Navbar() {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 sticky top-0 z-30">
      {/* Brand */}
      <div className="flex items-center gap-2 text-indigo-600 font-bold text-xl">
        <WiDaySunny className="text-3xl" />
        <span>SkyGuard AI</span>
      </div>

      {/* Right section */}
      <div className="flex items-center gap-4">
        <button className="relative p-2 text-gray-500 hover:text-indigo-600 transition">
          <FiBell className="text-xl" />
          <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-red-500" />
        </button>
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-semibold text-sm">
            A
          </div>
          <span className="text-sm text-gray-700 font-medium hidden sm:inline">
            Admin
          </span>
        </div>
      </div>
    </header>
  );
}

