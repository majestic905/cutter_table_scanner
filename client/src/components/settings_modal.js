import {useCallback, useEffect, useState} from "react";
import useFetch from "../hooks/useFetch";
import cx from "classnames";


const SettingsModal = ({closeModal}) => {
    const [data, setData] = useState();

    const [{isLoading, response, error}, doFetch] = useFetch('/api/cameras');  // for both GET and POST

    useEffect(doFetch, [doFetch]);

    useEffect(() => {
        if (response !== undefined && !data) { // GET
            setData(JSON.stringify(response, null, 2));
        } else if (response !== undefined && data) // POST
            closeModal();
    }, [response, setData, closeModal]);

    const doSubmit = useCallback(ev => {
        ev.preventDefault();

        doFetch({
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: ev.target.elements.settings.value
        });
    }, [doFetch]);

    const btnClassName = cx("btn btn-primary float-right mr-2", {loading: isLoading});

    return (
        <form className="modal active" onSubmit={doSubmit}>
            <span className="modal-overlay" onClick={closeModal}/>
            <div className="modal-container modal-fullheight">
                <div className="modal-header">
                    <button type="button" className="btn btn-link float-right" onClick={closeModal}>Закрыть</button>
                    <input type="submit" className={btnClassName} value="Отправить"/>

                    <div className="modal-title h5">Настройки</div>
                </div>
                <ul className="mt-0">
                   <li className="mt-0">
                       Значения table_section_size (миллиметры) напрямую в программе не используются, они здесь для того чтобы были.
                   </li>
                   <li className="mt-0">
                       Значения projected_image_size (пиксели) используются; задаются вручную; должны быть строго пропорциональны значениям table_section_size!
                   </li>
               </ul>
                {error && <div className="modal-header pt-0">
                     <div className="toast toast-error">{error}</div>
                </div>}
                <div className="modal-body pt-0">
                    {data && <textarea id="settings" name="settings" className="form-input" defaultValue={data}/>}
                    {isLoading && <div className="loading loading-lg"/>}
                </div>
            </div>
        </form>
    )
};


export default SettingsModal;