use cpython::py_module_initializer;

py_module_initializer!(uInterface, |py, m| {
    m.add(py, "__doc__", "Module documentation string")?;
    Ok(())
});