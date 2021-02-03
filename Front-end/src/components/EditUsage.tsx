import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import 'react-dropdown/style.css';

const EditUsage: React.FC = () => {

    const { id } = useParams<{ id: string }>();
    const [usage, setUsage] = useState<any>([])
    const [filament_data, setFilamentData] = useState<any>([])
    const [filament_detail, setFilamentDetail] = useState<any>([])
    const [user_data, setUserData] = useState<any>([])
    const [change, setChange] = useState<any>({
        additional_cost: 0,
        filament_cost: 0,
        total_cost: 0
    });

    const { owner, file_name, print_time, time_stamp, print_status, printer_name, operating_cost, printer_cost }: any = change;
    let { filament_cost, total_cost }: any = change
    let { filament_weight, filament_price, filament_name, additional_cost, filament_used }: any = filament_data

    filament_cost = (((parseFloat(filament_data.filament_price) / parseFloat(filament_data.filament_weight)) * parseFloat(filament_data.filament_used)).toFixed(2))
    console.log(filament_cost)
    total_cost = ((parseFloat(filament_cost) + parseFloat(change.printer_cost) + parseFloat(change.operating_cost) + (parseFloat(filament_data.additional_cost))).toFixed(2))


    const onInputChange = (e: any) => {
        const newChange = { ...filament_data, [e.target.name]: e.target.value }
        setFilamentData(newChange)
    }

    const handleFilament = (event: any) => {
        console.log(event.target.value)
        const set_filament = event.target.value
        var filament_select = filament_detail.filter(function (item: { filament_name: string; }) {
            return item.filament_name === set_filament;
        });
        console.log(filament_select)
        filament_weight = filament_select[0].filament_weight
        filament_price = filament_select[0].filament_price
        filament_name = filament_select[0].filament_name
        setFilamentData({ filament_weight, filament_price, filament_name, additional_cost, filament_used })
    }
    const callsetusage = () => {
        user_data.filament_cost = (parseFloat(user_data.filament_cost) + (parseFloat(filament_cost) - parseFloat(usage.filament_cost))).toFixed(2)
        user_data.additional_cost = (parseFloat(user_data.additional_cost) + (parseFloat(additional_cost) - parseFloat(usage.additional_cost))).toFixed(2)
        user_data.total_cost = ((parseFloat(user_data.filament_cost) + parseFloat(user_data.printer_cost) + parseFloat(user_data.operating_cost) + (parseFloat(user_data.additional_cost))).toFixed(2))
        setUserData(user_data)
        setUsage({ ...change, ...filament_data, filament_cost, total_cost })
    };

    useEffect(() => {
        loadUsage(); loadFilament(); loadUser();
    }, [owner]);

    const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log(usage)
        try {
            await axios.put(`http://localhost:8080/api/usage/${id}`, usage);
            console.log(user_data)
            await axios.put(`http://localhost:8080/api/user/${owner}`, user_data);
            alert("Usage detail updated")
        }
        catch (err) {
            alert(err.message)
        }
    };

    const loadUser = async () => {
        const result = await axios.get(`http://localhost:8080/api/user/${owner}`);
        setUserData(result.data);
    };


    const loadUsage = async () => {
        const result = await axios.get(`http://localhost:8080/api/usage/${id}`);
        setUsage(result.data);
        setChange(result.data);
        setFilamentData(result.data)

    };

    const loadFilament = async () => {
        const filament_result = await axios.get(`http://localhost:8080/api/filament`);
        console.log(filament_result.data)
        setFilamentDetail(filament_result.data)
    }
    return (
        <div className="container">
            <h1 className="text-center mt-5">Overview</h1>
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
            <form onSubmit={e => onSubmit(e)}>
                <div className="mx-auto mt-4 p-4 shadow ">
                    <h2 className="text-center mb-4">Edit Usage Details</h2>


                    <div className="form-row">
                        <div className="col-md-4">
                            <div className="">
                                <label htmlFor="select-filament">Filament Type</label>
                            </div>
                            <select className="custom-select has-tooltip"
                                name="select-filament" id="select-filament" data-tooltip="Which type of filament did you use?" onChange={handleFilament} value={filament_name} data-tippy-placement="top">
                                <option value="PLA" >PLA</option>
                                <option value="PETG">PETG</option>
                                <option value="ASA">ASA</option>
                                <option value="PC-Blend">PC-Blend</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div className="col-md-4 mb-3">
                            <label htmlFor="filament_price">Filament price (€)</label>
                            <input type="number"
                                step=".01"
                                className="form-control"
                                name="filament_price" placeholder="Filament price"
                                onChange={e => onInputChange(e)}
                                value={filament_price} required />
                        </div>
                        <div className="col-md-4 mb-3">
                            <label htmlFor="filament_weight">Filament weight (g)</label>
                            <input type="number"
                                step=".01"
                                className="form-control"
                                name="filament_weight" placeholder="Filament weight"
                                onChange={e => onInputChange(e)}
                                value={filament_weight} required />
                        </div>
                        <div className="col-md-4 mb-3">
                            <label htmlFor="filament_used">Filament used (g)</label>
                            <input type="number"
                                step=".01"
                                className="form-control"
                                name="filament_used" placeholder="Filament used"
                                onChange={e => onInputChange(e)}
                                value={filament_used} required />
                        </div>
                        <div className="col-md-4 mb-3">
                            <label htmlFor="additional_cost">Additional cost (€)</label>
                            <input type="number"
                                step=".01"
                                className="form-control"
                                onChange={e => onInputChange(e)}
                                name="additional_cost" placeholder="Additional cost"
                                value={additional_cost} required />
                        </div>
                    </div>
                    <div className="text-center">
                        <button className="btn btn-warning" onClick={callsetusage}>Update</button>
                    </div>
                </div>
            </form>
        </div >
    );
};

export default EditUsage;
