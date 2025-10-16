import React, { useState, useEffect } from "react";

export default function BackendTest() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // const API_URL = import.meta.env.VITE_API_URL

  // Update this URL to match your backend API endpoint
  // const API_URL = import.meta.env.VITE_API_URL || "http://192.168.50.113:8000/api/hello/";
  const API_URL = "http://192.168.50.113:8000/api/hello/";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(API_URL);
        if (!res.ok) {
          throw new Error(`Backend returned status ${res.status}`);
        }
        const json = await res.json();
        setData(json);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="p-6 text-center">
      <h1 className="text-2xl font-bold mb-4 text-blue-600">🔗 Backend Connectivity Test</h1>
      {loading && <p className="text-gray-500">Loading...</p>}
      {error && <p className="text-red-500">❌ Error: {error}</p>}
      {data && (
        <pre className="bg-gray-800 p-4 rounded-md border border-gray-200">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  );
}
