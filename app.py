import streamlit as st
import struct

st.set_page_config(page_title="Conversor de Bases + IEEE754", layout="centered")

# ------------------------------------------------------------
# IEEE754
# ------------------------------------------------------------

def float_to_ieee754_32(num):
    bits = struct.unpack('!I', struct.pack('!f', num))[0]
    b = f"{bits:032b}"
    return b[0], b[1:9], f"1.{b[9:]}", b

def float_to_ieee754_64(num):
    bits = struct.unpack('!Q', struct.pack('!d', num))[0]
    b = f"{bits:064b}"
    return b[0], b[1:12], f"1.{b[12:]}", b

def ieee754_32_to_float(bitstring):
    bits = int(bitstring, 2)
    return struct.unpack('!f', struct.pack('!I', bits))[0]


# ------------------------------------------------------------
# Converters
# ------------------------------------------------------------

def valor_do_digito(d):
    if d.isdigit():
        return int(d)
    return 10 + ord(d) - ord('A')

def converter_fracionario(valor, base):
    valor = valor.replace(",", ".")
    sinal = -1 if valor.startswith("-") else 1

    if valor.startswith("-"):
        valor = valor[1:]

    if "." not in valor:
        return sinal * int(valor, base)

    parte_int, parte_frac = valor.split(".")
    inteiro = int(parte_int, base) if parte_int else 0

    frac = 0
    for i, d in enumerate(parte_frac, start=1):
        frac += valor_do_digito(d) / (base ** i)

    return sinal * (inteiro + frac)

def converter_para_decimal(base, valor):
    valor = valor.strip().upper()
    if base == 10:
        return float(valor.replace(",", "."))
    return converter_fracionario(valor, base)


# ------------------------------------------------------------
# INTERFACE STREAMLIT
# ------------------------------------------------------------

st.title("🔢 Conversor de Bases + IEEE754")
st.write("Use no celular ou computador. Basta digitar e converter!")

base = st.selectbox(
    "Escolha a base do número digitado:",
    [
        ("Binário (2)", 2),
        ("Octal (8)", 8),
        ("Decimal (10)", 10),
        ("Hexadecimal (16)", 16),
        ("IEEE754 (32 bits)", 754)
    ],
    format_func=lambda x: x[0]
)[1]

valor = st.text_input("Digite o número:")

if st.button("Converter"):
    if not valor:
        st.error("Digite um valor!")
    else:
        try:
            # Entrada IEEE754 bruta
            if base == 754:
                bits = valor.replace(" ", "")
                if len(bits) != 32:
                    st.error("IEEE754 deve ter exatamente 32 bits.")
                else:
                    numero = ieee754_32_to_float(bits)
                    st.success(f"Decimal: **{numero}**")

            else:
                numero = converter_para_decimal(base, valor)
                st.success(f"Decimal: **{numero}**")

            # Inteiras
            st.subheader("📌 Conversões inteiras")

            try:
                inteiro = int(numero)
                st.write(f"**Binário:** {bin(inteiro)[2:]}")
                st.write(f"**Octal:** {oct(inteiro)[2:]}")
                st.write(f"**Hexadecimal:** {hex(inteiro)[2:].upper()}")
            except:
                st.info("Número fracionário → conversões inteiras indisponíveis.")

            # IEEE754
            st.subheader("💻 IEEE754")

            num_float = float(numero)

            s, e, m, b = float_to_ieee754_32(num_float)
            st.markdown("### IEEE754 (32 bits)")
            st.code(f"Sinal    : {s}\nExpoente : {e}\nMantissa : {m}\nBits     : {b}")

            s, e, m, b = float_to_ieee754_64(num_float)
            st.markdown("### IEEE754 (64 bits)")
            st.code(f"Sinal    : {s}\nExpoente : {e}\nMantissa : {m}\nBits     : {b}")

        except Exception as e:
            st.error(f"Erro: {e}")
