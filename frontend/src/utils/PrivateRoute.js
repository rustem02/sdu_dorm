import { Navigate } from 'react-router-dom';
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';

const PrivateRoute = ({ children }) => {
    const { user } = useContext(AuthContext);

    // Если нет user, перенаправляем на страницу входа
    if (!user) {
        return <Navigate to="/" replace />;
    }

    // Если пользователь аутентифицирован, рендерим детей (children)
    return children;
};

export default PrivateRoute;
