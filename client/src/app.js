import {useState, useEffect} from "react";
import useFetch from "./hooks/useFetch";

import ScansList from "./components/scans_list";
import Scan from "./components/scan";

import './app.scss';



function App() {
    const [selectedScan, setSelectedScan] = useState(null);

    const [{isLoading, response, error}, loadScans] = useFetch("/api/scans");

    useEffect(loadScans, [loadScans]);

    useEffect(() => {
        if (response && response.scans.length > 0)
            setSelectedScan(response.scans[0]);
        else if (error)
            alert(`Ошибка при загрузке списка: ${error}`);
    }, [response, error]);

    if (isLoading && !response)
        return <div className="loading"/>;

    // ------------

    return (
        <main className="container">
            <div className="columns">
                <div className="column col-3" id="column-left">
                    <ScansList scans={response?.scans} loadScans={loadScans}
                           selectedScan={selectedScan} selectScan={setSelectedScan}
                    />
                </div>

                <div className="divider-vert"/>

                <div className="column" id="column-right">
                    <Scan loadScans={loadScans} selectedScan={selectedScan} />
                </div>
            </div>
        </main>
    );
}

export default App;
