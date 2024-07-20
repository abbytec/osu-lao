'use client';

import { signIn, signOut, useSession } from 'next-auth/react';

export default function HomePage() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <p>Cargando...</p>;
  }

  return (
    <div>
      {!session && (
        <>
          <p>No estás logueado</p>
          <button onClick={() => signIn('osu')}>Login con osu!</button>
        </>
      )}
      {session?.user && (
        <>
          <p>Logueado como {session.user.name}</p>
          <button onClick={() => signOut()}>Logout</button>
        </>
      )}
    </div>
  );
}
