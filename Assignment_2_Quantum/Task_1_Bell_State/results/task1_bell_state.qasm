OPENQASM 2.0;
qreg q[2];
creg m_c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> m_c[0];
measure q[1] -> m_c[1];
