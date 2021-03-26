import {useCallback, useEffect} from "react";
import useModal from "../hooks/useModal";
import useFetch from "../hooks/useFetch";
import SettingsModal from "./settings_modal";


const Header = ({getScan}) => {
    const {isOpened, closeModal, openModal} = useModal();

    const [{isLoading, response, error}, doFetch] = useFetch('/api/scan');

    const requestScan = useCallback(type => {
        doFetch({method: 'POST', searchParams: {type}, timeout: 50000});
    }, [doFetch]);

    useEffect(() => {
        if (response)
            alert('Сканирование выполнено');
        else if (error)
            alert(`Произошла ошибка, сканирование не выполнено: ${error}`);

        if (response || error)
            getScan();
    }, [response, error, getScan]);

    return (
        <header className="navbar">
            <section className="navbar-section">
                <button className="btn btn-primary mr-2" onClick={() => requestScan('snapshot')}>
                    Сканировать
                </button>

                <button className="btn btn-primary mr-2" onClick={() => requestScan('calibration')}>
                    Калибровка точек
                </button>

                <button type="button" className='btn mr-2' onClick={openModal}>
                    Настройки
                </button>

                <button type="button" className='btn'>
                    Lensfun
                </button>
            </section>

            {isOpened && <SettingsModal closeModal={closeModal} />}
        </header>
    )
}

export default Header;