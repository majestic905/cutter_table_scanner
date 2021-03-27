import {useCallback, useEffect} from "react";
import cx from "classnames";
import useModal from "../hooks/useModal";
import useFetch from "../hooks/useFetch";
import SettingsModal from "./settings_modal";
import LensfunModal from "./lensfun_modal";


const Header = ({getScan}) => {
    const {isOpened: isOpenedSettings, closeModal: closeModalSettings, openModal: openModalSettings} = useModal();
    const {isOpened: isOpenedLensfun, closeModal: closeModalLensfun, openModal: openModalLensfun} = useModal();

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
                <button className={cx("btn btn-primary mr-2", {loading: isLoading})}
                        onClick={() => requestScan('snapshot')}
                >
                    Сканировать
                </button>

                <button className={cx("btn btn-primary mr-2", {loading: isLoading})}
                        onClick={() => requestScan('calibration')}
                >
                    Калибровка точек
                </button>

                <button type="button" className={cx('btn mr-2', {loading: isLoading})}
                        onClick={openModalSettings}
                >
                    Настройки
                </button>

                <button type="button" className={cx('btn', {loading: isLoading})}
                        onClick={openModalLensfun}
                >
                    Lensfun
                </button>
            </section>

            {isOpenedSettings && <SettingsModal closeModal={closeModalSettings} />}
            {isOpenedLensfun && <LensfunModal closeModal={closeModalLensfun} />}
        </header>
    )
}

export default Header;