import {useCallback, useEffect, useState} from "react";
import useFetch from "../hooks/useFetch";
import cx from "classnames";


function getIndentedJSON(json, space = 4) {
    const replacer = function(key, value) {
       if (value instanceof Array)
          return JSON.stringify(value);
       return value;
    };

    return JSON.stringify(json, replacer, space)
        .replace(/\"\[/g, '[')
        .replace(/\]\"/g, ']');
}


const SettingsModal = ({closeModal}) => {
    const [data, setData] = useState();

    const [{isLoading, response, error}, doFetch] = useFetch('/api/settings');  // for both GET and POST

    useEffect(doFetch, [doFetch]);

    useEffect(() => {
        if (response !== undefined && !data) { // GET
            setData(getIndentedJSON(response));
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
        <form className="modal active" id="settings-modal" onSubmit={doSubmit}>
            <span className="modal-overlay" onClick={closeModal}/>
            <div className="modal-container modal-fullheight">
                <div className="modal-header">
                    <button type="button" className="btn btn-link float-right" onClick={closeModal}>Закрыть</button>
                    <input type="submit" className={btnClassName} value="Отправить"/>

                    <div className="modal-title h5">Настройки</div>
                </div>
                <ul className="mt-0">
                   <li className="mt-0">
                       Значения real_size (миллиметры) напрямую в программе не используются, они здесь для того чтобы были.
                   </li>
                   <li className="mt-0">
                       Значения projection_image_size (пиксели) используются; задаются вручную; должны быть строго пропорциональны значениям real_size!
                   </li>
               </ul>
                {error && <div className="modal-header pt-0">
                     <div className="toast toast-error">{error}</div>
                </div>}
                <div className="modal-body pt-0">
                    {data && <textarea name="settings" defaultValue={data} className="form-input"/>}
                    {!data && <div className="loading loading-lg"/>}
                </div>
            </div>
        </form>
    )
};


export default SettingsModal;