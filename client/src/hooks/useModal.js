import {useState, useCallback} from 'react'


const useModal = (defaultIsOpened = false) => {
    const [isOpened, setIsOpened] = useState(defaultIsOpened);

    const openModal = useCallback(() => setIsOpened(true), [setIsOpened]);
    const closeModal = useCallback(() => setIsOpened(false), [setIsOpened]);
    const toggleModal = useCallback(() => setIsOpened(isOpened => !isOpened), [setIsOpened])

    return {openModal, closeModal, toggleModal, isOpened};
};

export default useModal;