import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

interface UsageData {
  owner: string,
  file_name: string,
  print_time: string,
  time_stamp: string,
  print_status: string,
  printer_name: string,
  filament_name: string,
  filament_price: string,
  filament_weight: string,
  filament_used: string,
  filament_cost: string,
  printer_cost: string,
  operating_cost: string,
  additional_cost: string,
  total_cost: string
}

const ViewUsage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [usage, setUsage] = useState<UsageData[]>([]);
  const { owner, file_name, print_time, time_stamp, print_status, printer_name, filament_cost, operating_cost, printer_cost, total_cost, filament_name, filament_price, filament_weight, filament_used, additional_cost }: any = usage;

  useEffect(() => {
    loadUsage();
  }, []);

  const loadUsage = async () => {
    const result = await axios.get(`http://localhost:8080/api/usage/${id}`);
    setUsage(result.data);
    console.log(result.data)
  };

  return (<div className="container">
    <h2 className="text-center mt-5">Overview</h2>
    <div className="verticaltable"><table>
      <tr>
        <th>User:</th>
        <td>{owner}</td>
      </tr>
      <tr>
        <th>File Name:</th>
        <td>{file_name}</td>
      </tr>
      <tr>
        <th>Print time (HH:MM:SS):</th>
        <td>{print_time}</td>
      </tr>
      <tr>
        <th>Time Stamp:</th>
        <td>{time_stamp}</td>
      </tr>
      <tr>
        <th>Print Status:</th>
        <td>{print_status}</td>
      </tr>
      <tr>
        <th>Print Name:</th>
        <td>{printer_name}</td>
      </tr>

      <tr>
        <th>Filament Name:</th>
        <td>{filament_name}</td>
      </tr>

      <tr>
        <th>Filament Price (€):</th>
        <td>{filament_price}</td>
      </tr>

      <tr>
        <th>Filament Used (g):</th>
        <td>{filament_used}</td>
      </tr>

      <tr>
        <th>Filament Weight (g):</th>
        <td>{filament_weight}</td>
      </tr>

      <tr>
        <th>Filament Cost (€):</th>
        <td><strong>{filament_cost}</strong></td>
      </tr>

      <tr>
        <th>Operating Cost (€):</th>
        <td><strong>{operating_cost}</strong></td>
      </tr>
      <tr>
        <th>Printer Cost (€):</th>
        <td><strong>{printer_cost}</strong></td>
      </tr>
      <tr>
        <th>Additional Cost (€):</th>
        <td><strong>{additional_cost}</strong></td>
      </tr>
      <tr>
        <th>Total Cost (€):</th>
        <td><strong>{total_cost}</strong></td>
      </tr>
    </table>
    </div>
  </div>
  );
};

export default ViewUsage;
