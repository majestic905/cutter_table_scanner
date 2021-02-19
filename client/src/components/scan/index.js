import {useCallback} from "react";
import Snapshot from './snapshot';
import Calibration from './calibration';


const ScanButton = ({onFinish}) => {
    const callApi = useCallback(() => {
        fetch('/api/scans', {method: 'POST'})
            .then(onFinish)
            .catch(error => console.error(error));
    }, [onFinish]);

    return (
        <button type="button" className='btn btn-sm bg-dark mr-2' onClick={callApi}>
            Полный скан
        </button>
    )
}


const CalibrateButton = ({onFinish}) => {
    const callApi = useCallback(() => {
        fetch('/api/cameras/projection_points/calibrate', {method: 'POST'})
            .then(onFinish)
            .catch(error => console.error(error));
    }, [onFinish]);

    return (
        <button type="button" className='btn btn-sm bg-dark mr-2' onClick={callApi}>
            Калибровка точек
        </button>
    )
}


const Scan = ({loadScans, selectedScan}) => {
    return (
        <div id="scan">
            <header>
                <ScanButton onFinish={loadScans}/>
                <CalibrateButton onFinish={loadScans}/>
            </header>

            <hr/>

            {!selectedScan && <p className="text-italic">Выберите скан из списка</p>}
            {selectedScan?.scanType === "SNAPSHOT" && <Snapshot scan={selectedScan}/>}
            {selectedScan?.scanType === "CALIBRATION" && <Calibration scan={selectedScan}/>}
        </div>
    )
}

export default Scan;