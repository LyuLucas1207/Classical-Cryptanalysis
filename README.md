# classical-cryptanalysis

古典密码破译。这份材料说明五种课堂上的古典密码为什么看起来像加密、实际上仍能被认出来并还原出明文开头的宝可梦名字。

Classical cryptanalysis. These notes explain why five classroom ciphers still leak enough structure to be recognized, and why each plaintext can be recovered far enough to read the Pokémon name at the start.

## 要回答的问题

1. **重合指数。** Caesar、仿射、Vigenère、Playfair 加密之后，重合指数相对明文会升高、降低，还是保持不变，以及原因。
2. **辨认密码。** 一组文件里有六行密文。在不解密的前提下，判断哪一行是哪一种密码。
3. **破译名字。** 每段明文都是一段宝可梦短评，而且一定以宝可梦名字开头。对每一行密文，找出这个名字，并说明用了什么方法。

六行里有五种密码：Caesar、仿射、Vigenère、Playfair 各一次，一次性密码本（OTP）用了两次，而且两次用的是同一条密钥。

## Questions

1. **Index of coincidence.** For Caesar, affine, Vigenère, and Playfair, say whether the ciphertext’s index of coincidence is higher, lower, or equal to the plaintext’s, and why.
2. **Identify the cipher.** A ciphertext file has six lines. Without decrypting, decide which line was produced by which cipher.
3. **Recover the name.** Every plaintext is a short Pokémon description and always begins with the Pokémon’s name. For each line, recover that name and explain the method.

The six lines use five ciphers: Caesar, affine, Vigenère, and Playfair once each, and a one-time pad twice, both times with the same key.

默认示例是第 80 组：`texts/ciphertexts_80.txt`。下文的行号、IC 和辨认结果都指这一份。第 0 组只是作业自带的对照，不是这份笔记的例子。

The default example is group 80: `texts/ciphertexts_80.txt`. Line numbers, IC values, and identifications below refer to that file. Group 0 is only the handout’s worked check, not the example used here.

## 五种密码

明文先被收成只含 `A`–`Z` 的大写字母：字母转成大写，空格、逗号、句号全部删掉。下面的加密都作用在这条字母串上。

### Caesar

每个字母沿字母表移动同一个整数 \(k\)，\(k\) 从 1 到 25。`A` 在 \(k = 1\) 时变成 `B`，到 `Z` 之后绕回 `A`。解密是反向移动 \(k\)。密钥空间只有 25 个，逐个尝试即可。它是单表替换：同一个明文字母永远变成同一个密文字母，所以英文字母频率原样留在密文里。

### 仿射（Affine）

加密是 \(E(x) = (ax + b) \bmod 26\)。\(x\) 是字母序号（`A` = 0 … `Z` = 25），密钥是一对 \((a, b)\)。\(a\) 必须与 26 互素，这样 \(a^{-1}\) 存在，解密才是单值的：\(D(y) = a^{-1}(y - b) \bmod 26\)。它仍是单表替换，字母频率的形状不变，只是哪个字母对应哪个频率被打乱了。

### Vigenère

密钥是一个英文单词。加密时按位置循环使用密钥字母当作移位量：第 \(i\) 个明文字母移动「密钥第 \(i \bmod L\) 个字母」那么多位，\(L\) 是密钥长度。同一个明文字母会因为落在密钥的不同位置而变成不同密文字母，字母频率被拉向均匀。密钥长度为 1 时，它退回 Caesar。

### Playfair

按字母对加密，不用单字母替换。作业里的准备步骤是：把每个 `J` 换成 `I`；相邻重复字母中间插入 `X`；保证长度为偶数，并且不超过 300。密钥是 `A`–`Z` 去掉 `J` 之后的一个随机排列，长度 25，排成 5×5 方阵。同一对里两个字母的去向取决于它们在方阵中的相对位置。密文字母表里不会出现 `J`。

### 一次性密码本（OTP）

每个字母先按 RFC 4648 Base32 编成 5 比特（字母表是 `A`–`Z` 和 `2`–`7`），再与一条伪随机密钥逐比特异或，结果再用同一套 Base32 编回字符。因此密文里可以出现数字 `2`–`7`。另外四种密码只输出 `A`–`Z`。

这里的 OTP 用了两次，密钥相同。两条密文异或后，密钥消掉，剩下的是两段明文的异或。明文又以已知形式的宝可梦名字开头，所以重复使用的密钥可以被对消，而不是被穷举。

## The five ciphers

Plaintext is reduced to uppercase `A`–`Z` only: letters are uppercased, and spaces, commas, and periods are deleted. Every cipher below operates on that letter string.

### Caesar

Every letter moves forward by the same integer \(k\), with \(k\) from 1 to 25. `A` with \(k = 1\) becomes `B`, and `Z` wraps to `A`. Decryption moves backward by \(k\). The key space has 25 values, so exhaustive search works. It is a monoalphabetic substitution: one plaintext letter always becomes one ciphertext letter, and English letter frequencies survive unchanged.

### Affine

Encryption is \(E(x) = (ax + b) \bmod 26\). \(x\) is the letter index (`A` = 0 … `Z` = 25), and the key is a pair \((a, b)\). \(a\) must be coprime to 26 so that \(a^{-1}\) exists and decryption is unique: \(D(y) = a^{-1}(y - b) \bmod 26\). This is still a monoalphabetic substitution. The shape of the frequency distribution stays; only the letter that carries each frequency changes.

### Vigenère

The key is an English word. Encryption cycles through the key letters as shift amounts: plaintext letter \(i\) shifts by the letter at position \(i \bmod L\), where \(L\) is the key length. The same plaintext letter becomes different ciphertext letters when it lands on different key positions, so the frequency distribution moves toward uniform. A key of length 1 is Caesar again.

### Playfair

Letters are encrypted in pairs. The preparation used here replaces every `J` with `I`, inserts `X` between consecutive identical letters, and forces an even length of at most 300. The key is a random permutation of `A`–`Z` without `J`, 25 characters, written as a 5×5 square. Where a pair goes depends on the two letters’ positions in that square. The ciphertext alphabet never contains `J`.

### One-time pad (OTP)

Each letter is encoded as 5 bits with the RFC 4648 Base32 alphabet (`A`–`Z` and `2`–`7`), XORed with a pseudorandom key, and encoded back with the same alphabet. Digits `2`–`7` can therefore appear. The other four ciphers emit only `A`–`Z`.

This OTP is used twice with the same key. XORing the two ciphertexts cancels the key and leaves the XOR of the two plaintexts. Because each plaintext opens with a Pokémon name, the reused pad can be cancelled rather than searched.

## 重合指数

重合指数衡量：随机抽两个字母，它们相同的可能性有多大。设字母 \(i\) 出现 \(n_i\) 次，全文长度是 \(N\)，字母表大小 \(c = 26\)：

\[
\mathrm{IC} = 26 \sum_{i} \frac{n_i}{N} \cdot \frac{n_i - 1}{N - 1}.
\]

英文散文的 IC 大约是 1.73。每个字母同等可能时，IC 是 1.00。

| 密码 | 密文 IC 相对明文 | 原因 |
| --- | --- | --- |
| Caesar | 相等 | 固定移位是字母表的一个置换，各字母出现次数不变 |
| 仿射 | 相等 | 一对一替换，频率分布整体被重新贴标签 |
| Vigenère | 更低 | 同一明文字母对应多个密文字母，分布更接近均匀。密钥长度为 1 时与 Caesar 相同，IC 不变 |
| Playfair | 更低 | 按字母对加密，单个字母的去向还取决于它的搭档，单字母频率被打散 |

OTP 不在这张表里。它的字母表含数字，和只含 `A`–`Z` 的 IC 不是同一套比较。

## Index of coincidence

The index of coincidence is the chance that two letters drawn at random are the same. If letter \(i\) occurs \(n_i\) times, the text length is \(N\), and the alphabet size is \(c = 26\):

\[
\mathrm{IC} = 26 \sum_{i} \frac{n_i}{N} \cdot \frac{n_i - 1}{N - 1}.
\]

English prose sits near 1.73. A uniform random string sits at 1.00.

| Cipher | Ciphertext IC vs. plaintext | Why |
| --- | --- | --- |
| Caesar | Equal | A fixed shift is a permutation of the alphabet, so the counts stay the same |
| Affine | Equal | A one-to-one substitution relabels the frequency distribution |
| Vigenère | Lower | One plaintext letter maps to several ciphertext letters, so the distribution moves toward uniform. Key length 1 is Caesar, and the IC stays the same |
| Playfair | Lower | Digram encryption makes a letter’s image depend on its partner, which breaks single-letter frequencies |

OTP is outside this table. Its alphabet includes digits, so its IC is not comparable with an `A`–`Z` text on the same scale.

## 怎样把六行对上号

以第 80 组为例。不需要先求出密钥。

| 行 | 密码 | 依据 |
| --- | --- | --- |
| 1 | Playfair | 唯一没有 `J` 的字母行 |
| 2 | Caesar 或仿射 | IC \(\times 26 = 1.79\)，靠近英文 1.73 |
| 3 | OTP | 含 Base32 数字 `2`–`7` |
| 4 | OTP | 含 Base32 数字 `2`–`7` |
| 5 | Caesar 或仿射 | IC \(\times 26 = 1.68\)，靠近英文 1.73 |
| 6 | Vigenère | IC \(\times 26 = 1.12\)，三行里离 1.73 最远、最接近随机 1.00 |

- **含数字 `2`–`7` 的两行是 OTP。** 只有 Base32 会写出这些数字。作业也说明 OTP 用了两次。
- **字母行里唯一没有 `J` 的那一行是 Playfair。** 密钥和明文都把 `J` 并进了 `I`。其余只含字母的行都会出现 `J`。
- **剩下三行用 IC 分开。** Caesar 和仿射的 IC 靠近英文（约 1.73）。Vigenère 的 IC 掉向 1.00，是三行里最接近随机串的那一行。
- Caesar 和仿射彼此都是单表替换，IC 分不开它们。频率直方图可以看分布是否仍像英文（Caesar 只是整表平移），仿射则是更一般的重标。逐个试 25 个 Caesar 移位，看结果是否像英文，也能把 Caesar 单独定下来。

## How the six lines are told apart

Group 80 is the default example. The key is not required.

| Line | Cipher | Why |
| --- | --- | --- |
| 1 | Playfair | Only letter-only line with no `J` |
| 2 | Caesar or affine | IC \(\times 26 = 1.79\), near English 1.73 |
| 3 | OTP | Contains Base32 digits `2`–`7` |
| 4 | OTP | Contains Base32 digits `2`–`7` |
| 5 | Caesar or affine | IC \(\times 26 = 1.68\), near English 1.73 |
| 6 | Vigenère | IC \(\times 26 = 1.12\), farthest from 1.73 and closest to random 1.00 |

- **The two lines that contain digits `2`–`7` are the OTP.** Only Base32 writes those digits. The handout also states that the OTP was used twice.
- **The only all-letter line with no `J` is Playfair.** Both the key and the plaintext fold `J` into `I`. The other letter-only lines contain `J`.
- **IC separates the remaining three.** Caesar and affine stay near English (about 1.73). Vigenère falls toward 1.00 and is the line closest to a random string.
- Caesar and affine are both monoalphabetic, so IC does not separate them. A frequency histogram shows whether the distribution is still English shifted as a block (Caesar) or relabeled more freely (affine). Trying all 25 Caesar shifts and reading the output as English also isolates Caesar.

## 明文从哪来

1. 151 段明文，对应前 151 只宝可梦，每段只用字母、逗号和句号，并且以宝可梦名字开头。这是已知明文：名字的位置和字符集是固定的。
2. 转成大写 `A`–`Z`，删掉其他字符。
3. 每个小组随机抽六段，分别用上面的密码加密。Caesar 的移位、仿射的 \((a, b)\)、Vigenère 的英文单词、Playfair 的 25 字母排列都是随机抽的。OTP 的密钥是伪随机的，并且在两段明文上重复使用。
4. 六行密文的顺序是打乱的。Caesar 可以出现在任意一行。

这份笔记默认用第 80 组：打开 `texts/ciphertexts_80.txt`，上面的行号就是这一份的 1–6 行。第 0 组没有分给任何人，只是作业自带的对照：`plaintexts_0.txt` 的第 \(j\) 行，用 `ciphers_and_keys_0.txt` 的第 \(j\) 行加密，得到 `ciphertexts_0.txt` 的第 \(j\) 行。

## Where the plaintext comes from

1. There are 151 plaintexts, one short description for each of the first 151 Pokémon, using only letters, commas, and periods, each starting with the Pokémon name. That opening name is known plaintext: its position and character set are fixed.
2. The text is converted to uppercase `A`–`Z`, and every other character is deleted.
3. Each group receives six plaintexts chosen at random and encrypted with the ciphers above. The Caesar shift, the affine pair \((a, b)\), the Vigenère word, and the 25-letter Playfair permutation are sampled at random. The OTP key is pseudorandom and is reused on two plaintexts.
4. The six ciphertext lines are written in a shuffled order. Caesar may sit on any line.

This write-up defaults to group 80: open `texts/ciphertexts_80.txt`; the line numbers above are that file’s six lines. Group 0 is unassigned and is only the handout’s check: line \(j\) of `plaintexts_0.txt`, encrypted with line \(j\) of `ciphers_and_keys_0.txt`, is line \(j\) of `ciphertexts_0.txt`.

## 文件

| 路径 | 内容 |
| --- | --- |
| `a1-cpen442.pdf` | 作业说明 |
| `texts/ciphertexts_80.txt` | **默认示例**：第 80 组密文 |
| `plaintexts_0.txt` | 第 0 组明文（作业对照，不是默认例子） |
| `ciphers_and_keys_0.txt` | 第 0 组密码名和密钥（作业对照） |
| `ciphertexts_0.txt` | 第 0 组密文（作业对照） |
| `texts/` | 各小组的密文文件 |
| `submission/` | 解答稿和字母频率图 |
