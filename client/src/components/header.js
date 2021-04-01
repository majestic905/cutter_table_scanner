import {useCallback, useEffect} from "react";
import cx from "classnames";
import useModal from "../hooks/useModal";
import useFetch from "../hooks/useFetch";
import SettingsModal from "./settings_modal";


const Header = ({getScan}) => {
    const {isOpened, closeModal, openModal} = useModal();

    const [{isLoading, response, error}, doFetch] = useFetch('/api/scan');

    const requestScan = useCallback(scanType => {
        doFetch({method: 'POST', searchParams: {scan_type: scanType}, timeout: 50000});
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
                        onClick={() => requestScan('capture')}
                >
                    Сделать фото
                </button>

                <button type="button" className={cx('btn mr-2', {loading: isLoading})}
                        onClick={openModal}
                >
                    Настройки
                </button>
            </section>

            {isOpened && <SettingsModal closeModal={closeModal} />}
        </header>
    )
}

export default Header;