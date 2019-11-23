import React, {useEffect, useState} from 'react';
import axios from 'axios';

const Todo = (props) => {
  const url = `https://jsonplaceholder.typicode.com/todos/${props.id}`;
  const [todo, setTodo] = useState(null);
  useEffect(() => {
    axios.get(url)
      .then(response => {
        setTodo(response.data)
      })
  });

  return (
    <h1>{todo ? todo.title : 'Loading'}</h1>
  );
}

export default Todo;