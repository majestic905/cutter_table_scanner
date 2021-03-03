import {useCallback, useEffect} from "react";
import useModal from "../../hooks/useModal";
import useFetch from "../../hooks/useFetch";
import Snapshot from './snapshot';
import Calibration from './calibration';
import SettingsModal from "../settings_modal";


const Scan = ({loadScans, selectedScan}) => {
    const {isOpened, closeModal, openModal} = useModal();

    const [{isLoading, response, error}, doFetch] = useFetch('/api/scans');

    const requestScan = useCallback(type => {
        doFetch({method: 'POST'}, `type=${type}`);
    }, [doFetch]);

    useEffect(() => {
        if (response)
            alert('Сканирование выполнено');
        else if (error) {
            alert(`Произошла ошибка, сканирование не выполнено: ${error}`);
        }

        if (response || error)
            loadScans();
    }, [response, error, loadScans]);

    return (
        <div id="scan">
            <header>
                <button className="btn btn-sm btn-primary mr-2" onClick={requestScan}>
                    Полный скан
                </button>

                <button className="btn btn-sm btn-primary mr-2" onClick={requestScan}>
                    Калибровка точек
                </button>

                <button type="button" className='btn btn-sm' onClick={openModal}>
                    Настройки
                </button>
            </header>

            <hr/>

            {!selectedScan && <p className="text-italic">Выберите скан из списка</p>}
            {selectedScan?.scanType === "SNAPSHOT" && <Snapshot scan={selectedScan}/>}
            {selectedScan?.scanType === "CALIBRATION" && <Calibration scan={selectedScan}/>}
            {isOpened && <SettingsModal closeModal={closeModal} />}
        </div>
    )
}

export default Scan;