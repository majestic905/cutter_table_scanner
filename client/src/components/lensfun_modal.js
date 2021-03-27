import {useCallback, useEffect, useState} from "react";
import useFetch from "../hooks/useFetch";
import cx from "classnames";


const LensfunModal = ({closeModal}) => {
    const [data, setData] = useState();

    const [{isLoading, response, error}, doFetch] = useFetch('/api/lensfun');  // for both GET and POST

    useEffect(doFetch, [doFetch]);

    useEffect(() => {
        if (response !== undefined && !data) { // GET
            setData(response.xml);
        } else if (response !== undefined && data) // POST
            closeModal();
    }, [response, setData, closeModal]);

    const doSubmit = useCallback(ev => {
        ev.preventDefault();

        doFetch({
            method: 'POST',
            headers: { 'Content-Type': 'text/xml; charset=utf-8' },
            body: ev.target.elements.lensfun.value
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

                    <div className="modal-title h5">Lensfun XML</div>
                </div>
                {error && <div className="modal-header pt-0">
                     <div className="toast toast-error">{error}</div>
                </div>}
                <div className="modal-body pt-0">
                    {data && <textarea name="lensfun" defaultValue={data} className="form-input"/>}
                    {!data && <div className="loading loading-lg"/>}
                </div>
            </div>
        </form>
    )
};


export default LensfunModal;