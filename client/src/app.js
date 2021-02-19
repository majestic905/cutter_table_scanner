import {useState, useEffect, useCallback} from "react";

import ScansList from "./components/scans_list";
import Scan from "./components/scan";

import './app.scss';



function App() {
    const [scans, setScans] = useState(null);
    const [selectedScan, setSelectedScan] = useState(null);

    const loadScans = useCallback(() => {
        setSelectedScan(null);

        fetch('/api/scans')
            .then(res => res.json())
            .then(data => {
                setScans(data.scans);
                console.log(data.scans);
                if (data.scans.length > 0)
                    setSelectedScan(data.scans[0]);
            })
            .catch(error => console.error(error));
    }, [setScans, setSelectedScan]);

    useEffect(loadScans, []);

    // ------------

    return (
        <main className="container">
            <div className="columns">
                <div className="column col-3" id="column-left">
                    <ScansList scans={scans} loadScans={loadScans}
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
